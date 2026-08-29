"""
LifeOS Authentication Service
"""

from datetime import datetime, timedelta
from backend.models.base import db
from backend.models.user import User, UserProfile, UserSession
from backend.models.settings import UserSettings, DashboardPreference
from backend.models.notification import NotificationPreference
from backend.security.password_hasher import hash_password, verify_password, validate_password_strength
from backend.security.validators import validate_email, validate_username, sanitize_string
from backend.security.auth_middleware import generate_jwt_token
from backend.models.audit import AuditLog

class AuthService:

    @staticmethod
    def register_user(data: dict) -> tuple:
        """Registers a new user account with default profile, settings, and notification preferences."""
        username = sanitize_string(data.get("username", ""))
        email = sanitize_string(data.get("email", "")).lower()
        password = data.get("password", "")
        full_name = sanitize_string(data.get("full_name", ""))

        if not validate_username(username):
            return False, "Invalid username. Must be 3-30 characters (letters, numbers, underscores)."
        if not validate_email(email):
            return False, "Invalid email address format."

        is_valid_pwd, msg = validate_password_strength(password)
        if not is_valid_pwd:
            return False, msg

        if User.query.filter_by(username=username).first():
            return False, "Username is already taken."
        if User.query.filter_by(email=email).first():
            return False, "Email address is already registered."

        role = data.get("role", "user")
        if role not in ["user", "admin"]:
            role = "user"

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role=role,
            is_active=True,
            is_verified=True
        )
        db.session.add(user)
        db.session.flush()

        # Create Profile
        profile = UserProfile(
            user_id=user.id,
            full_name=full_name or username,
            bio="Welcome to my LifeOS platform!",
            timezone="UTC"
        )
        db.session.add(profile)

        # Create Settings & Preferences
        settings = UserSettings(user_id=user.id)
        dashboard_pref = DashboardPreference(user_id=user.id)
        notif_pref = NotificationPreference(user_id=user.id)
        
        db.session.add(settings)
        db.session.add(dashboard_pref)
        db.session.add(notif_pref)

        # Audit Log
        audit = AuditLog(
            user_id=user.id,
            action="USER_REGISTERED",
            resource_type="user",
            resource_id=str(user.id),
            details=f"User registered with username: {username}"
        )
        db.session.add(audit)

        db.session.commit()

        token = generate_jwt_token(user)
        return True, {
            "token": token,
            "user": user.to_dict()
        }

    @staticmethod
    def login_user(data: dict, ip_address: str = None, user_agent: str = None) -> tuple:
        """Authenticates user, checks lockouts, and generates session token."""
        login_input = sanitize_string(data.get("username") or data.get("email") or "").strip()
        password = data.get("password", "")

        if not login_input or not password:
            return False, "Username/Email and Password are required."

        user = User.query.filter((User.username == login_input) | (User.email == login_input.lower())).first()
        if not user or user.is_deleted:
            return False, "Invalid credentials provided."

        if not user.is_active:
            return False, "Account has been deactivated. Please contact support."

        if user.is_locked():
            return False, "Account locked due to multiple failed login attempts. Try again later."

        if not verify_password(user.password_hash, password):
            user.record_failed_login()
            db.session.commit()
            return False, "Invalid credentials provided."

        user.update_login_timestamp()

        session_token = generate_jwt_token(user)
        user_session = UserSession(
            user_id=user.id,
            session_token=session_token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=datetime.utcnow() + timedelta(days=7),
            is_active=True
        )
        db.session.add(user_session)

        # Audit Log
        audit = AuditLog(
            user_id=user.id,
            action="USER_LOGIN",
            resource_type="session",
            resource_id=str(user_session.id),
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(audit)
        db.session.commit()

        return True, {
            "token": session_token,
            "user": user.to_dict()
        }

    @staticmethod
    def change_password(user_id: int, old_password: str, new_password: str) -> tuple:
        """Changes password for an authenticated user."""
        user = User.query.get(user_id)
        if not user:
            return False, "User not found."

        if not verify_password(user.password_hash, old_password):
            return False, "Current password is incorrect."

        is_valid, msg = validate_password_strength(new_password)
        if not is_valid:
            return False, msg

        user.password_hash = hash_password(new_password)
        
        audit = AuditLog(
            user_id=user.id,
            action="PASSWORD_CHANGED",
            resource_type="user",
            resource_id=str(user.id)
        )
        db.session.add(audit)
        db.session.commit()

        return True, "Password successfully updated."
