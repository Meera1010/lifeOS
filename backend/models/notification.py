"""
LifeOS Notification System Models
"""

from datetime import datetime
from backend.models.base import db, TimestampMixin, SerializerMixin
from backend.app.constants import NotificationType, NotificationSeverity

class Notification(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), default=NotificationType.SYSTEM_ALERT.value, nullable=False, index=True)
    severity = db.Column(db.String(20), default=NotificationSeverity.INFO.value, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)
    read_at = db.Column(db.DateTime, nullable=True)
    action_url = db.Column(db.String(255), nullable=True)
    entity_type = db.Column(db.String(50), nullable=True) # task, habit, goal, finance, etc.
    entity_id = db.Column(db.Integer, nullable=True)

    def mark_as_read(self):
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.add(self)


class NotificationPreference(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "notification_preferences"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    task_reminders = db.Column(db.Boolean, default=True, nullable=False)
    habit_reminders = db.Column(db.Boolean, default=True, nullable=False)
    goal_deadlines = db.Column(db.Boolean, default=True, nullable=False)
    budget_alerts = db.Column(db.Boolean, default=True, nullable=False)
    study_reminders = db.Column(db.Boolean, default=True, nullable=False)
    achievement_unlocked = db.Column(db.Boolean, default=True, nullable=False)
    system_alerts = db.Column(db.Boolean, default=True, nullable=False)
    email_notifications = db.Column(db.Boolean, default=False, nullable=False)
