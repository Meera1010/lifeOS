"""
LifeOS User, UserProfile, and UserSession Models
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.base import db, TimestampMixin, SoftDeleteMixin, SerializerMixin
from backend.app.constants import UserRole

class User(db.Model, TimestampMixin, SoftDeleteMixin, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default=UserRole.USER.value, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)

    # Relationships
    profile = db.relationship("UserProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    settings = db.relationship("UserSettings", backref="user", uselist=False, cascade="all, delete-orphan")
    dashboard_pref = db.relationship("DashboardPreference", backref="user", uselist=False, cascade="all, delete-orphan")
    sessions = db.relationship("UserSession", backref="user", cascade="all, delete-orphan")
    tasks = db.relationship("Task", backref="user", cascade="all, delete-orphan")
    habits = db.relationship("Habit", backref="user", cascade="all, delete-orphan")
    goals = db.relationship("Goal", backref="user", cascade="all, delete-orphan")
    calendar_events = db.relationship("CalendarEvent", backref="user", cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", backref="user", cascade="all, delete-orphan")
    budgets = db.relationship("Budget", backref="user", cascade="all, delete-orphan")
    savings_goals = db.relationship("SavingsGoal", backref="user", cascade="all, delete-orphan")
    courses = db.relationship("Course", backref="user", cascade="all, delete-orphan")
    study_sessions = db.relationship("StudySession", backref="user", cascade="all, delete-orphan")
    focus_sessions = db.relationship("FocusSession", backref="user", cascade="all, delete-orphan")
    journal_entries = db.relationship("JournalEntry", backref="user", cascade="all, delete-orphan")
    user_achievements = db.relationship("UserAchievement", backref="user", cascade="all, delete-orphan")
    notifications = db.relationship("Notification", backref="user", cascade="all, delete-orphan")
    audit_logs = db.relationship("AuditLog", backref="user", cascade="all, delete-orphan")

    def set_password(self, password):
        """Hashes password with Werkzeug pbkdf2:sha256."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies plain password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == UserRole.ADMIN.value

    def update_login_timestamp(self):
        self.last_login = datetime.utcnow()
        self.failed_login_attempts = 0
        self.locked_until = None
        db.session.add(self)

    def record_failed_login(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            # Lock out for 15 minutes
            from datetime import timedelta
            self.locked_until = datetime.utcnow() + timedelta(minutes=15)
        db.session.add(self)

    def is_locked(self):
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False

    def to_dict(self, exclude=None, include_relationships=False):
        ex = exclude or []
        ex.append("password_hash")
        data = super().to_dict(exclude=ex)
        if self.profile:
            data["profile"] = self.profile.to_dict()
        return data


class UserProfile(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(30), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    occupation = db.Column(db.String(100), nullable=True)
    timezone = db.Column(db.String(50), default="UTC", nullable=False)
    life_motto = db.Column(db.String(255), nullable=True)
    total_life_score = db.Column(db.Float, default=0.0, nullable=False)


class UserSession(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "user_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def is_expired(self):
        return datetime.utcnow() >= self.expires_at
