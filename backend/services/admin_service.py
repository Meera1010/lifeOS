"""
LifeOS Administrator Panel Service
"""

from datetime import datetime
from backend.models.base import db
from backend.models.user import User, UserProfile
from backend.models.audit import AuditLog
from backend.models.task import Task
from backend.models.habit import Habit
from backend.models.goal import Goal
from backend.models.finance import Transaction
from backend.security.password_hasher import hash_password
from backend.security.validators import sanitize_string, validate_email, validate_username

class AdminService:

    @staticmethod
    def list_all_users(page: int = 1, per_page: int = 20, search_term: str = None) -> tuple:
        query = User.query.filter_by(is_deleted=False)
        if search_term:
            term = f"%{search_term}%"
            query = query.filter((User.username.ilike(term)) | (User.email.ilike(term)))

        total = query.count()
        users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False).items
        return [u.to_dict() for u in users], total

    @staticmethod
    def create_user_by_admin(admin_user_id: int, data: dict) -> tuple:
        username = sanitize_string(data.get("username", ""))
        email = sanitize_string(data.get("email", "")).lower()
        password = data.get("password", "")
        role = data.get("role", "user")

        if not validate_username(username):
            return False, "Invalid username."
        if not validate_email(email):
            return False, "Invalid email address."
        if User.query.filter_by(username=username).first():
            return False, "Username already taken."
        if User.query.filter_by(email=email).first():
            return False, "Email already in use."

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password or "DefaultPass123!"),
            role=role,
            is_active=True,
            is_verified=True
        )
        db.session.add(user)
        db.session.flush()

        profile = UserProfile(user_id=user.id, full_name=username)
        db.session.add(profile)

        audit = AuditLog(
            user_id=admin_user_id,
            action="ADMIN_CREATED_USER",
            resource_type="user",
            resource_id=str(user.id),
            details=f"Admin created user {username} with role {role}."
        )
        db.session.add(audit)

        db.session.commit()
        return True, user.to_dict()

    @staticmethod
    def toggle_user_active_status(admin_user_id: int, target_user_id: int) -> tuple:
        if admin_user_id == target_user_id:
            return False, "Administrators cannot disable their own account."

        user = User.query.get(target_user_id)
        if not user or user.is_deleted:
            return False, "Target user not found."

        user.is_active = not user.is_active
        
        audit = AuditLog(
            user_id=admin_user_id,
            action="ADMIN_TOGGLED_USER_STATUS",
            resource_type="user",
            resource_id=str(user.id),
            details=f"User active status changed to {user.is_active}."
        )
        db.session.add(audit)
        db.session.commit()

        return True, user.to_dict()

    @staticmethod
    def delete_user_by_admin(admin_user_id: int, target_user_id: int) -> tuple:
        if admin_user_id == target_user_id:
            return False, "Administrators cannot delete their own account."

        user = User.query.get(target_user_id)
        if not user:
            return False, "Target user not found."

        user.soft_delete()

        audit = AuditLog(
            user_id=admin_user_id,
            action="ADMIN_DELETED_USER",
            resource_type="user",
            resource_id=str(user.id),
            details=f"User {user.username} deleted by admin."
        )
        db.session.add(audit)
        db.session.commit()

        return True, "User successfully deleted."

    @staticmethod
    def get_system_audit_logs(page: int = 1, per_page: int = 50) -> tuple:
        query = AuditLog.query.order_by(AuditLog.timestamp.desc())
        total = query.count()
        logs = query.paginate(page=page, per_page=per_page, error_out=False).items
        return [l.to_dict() for l in logs], total

    @staticmethod
    def get_system_statistics() -> dict:
        return {
            "total_registered_users": User.query.filter_by(is_deleted=False).count(),
            "active_users": User.query.filter_by(is_active=True, is_deleted=False).count(),
            "total_tasks_created": Task.query.count(),
            "total_habits_tracked": Habit.query.count(),
            "total_goals_defined": Goal.query.count(),
            "total_transactions_logged": Transaction.query.count(),
            "system_status": "Healthy",
            "server_time": datetime.utcnow().isoformat()
        }
