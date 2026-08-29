"""
LifeOS Focus & Productivity System Models
"""

from datetime import datetime, date
from backend.models.base import db, TimestampMixin, SerializerMixin
from backend.app.constants import FocusSessionType

class FocusSession(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "focus_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=True)
    
    session_type = db.Column(db.String(30), default=FocusSessionType.POMODORO.value, nullable=False)
    duration_minutes = db.Column(db.Integer, default=25, nullable=False)
    actual_minutes = db.Column(db.Integer, default=25, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    productivity_rating = db.Column(db.Integer, default=5, nullable=False) # 1 to 5
    distraction_count = db.Column(db.Integer, default=0, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=True, nullable=False)

    distractions = db.relationship("DistractionLog", backref="focus_session", cascade="all, delete-orphan", lazy="dynamic")


class DistractionLog(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "focus_distraction_logs"

    id = db.Column(db.Integer, primary_key=True)
    focus_session_id = db.Column(db.Integer, db.ForeignKey("focus_sessions.id"), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), default="Internal", nullable=False) # Social Media, Phone, Internal Thought, Interrupt
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class PomodoroSetting(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "focus_pomodoro_settings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    work_duration = db.Column(db.Integer, default=25, nullable=False)
    short_break = db.Column(db.Integer, default=5, nullable=False)
    long_break = db.Column(db.Integer, default=15, nullable=False)
    sessions_until_long_break = db.Column(db.Integer, default=4, nullable=False)
    auto_start_breaks = db.Column(db.Boolean, default=False, nullable=False)
    auto_start_pomodoros = db.Column(db.Boolean, default=False, nullable=False)
    sound_enabled = db.Column(db.Boolean, default=True, nullable=False)


class DailyFocusSummary(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "focus_daily_summaries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    summary_date = db.Column(db.Date, default=date.today, nullable=False, index=True)
    total_focus_minutes = db.Column(db.Integer, default=0, nullable=False)
    completed_sessions = db.Column(db.Integer, default=0, nullable=False)
    total_distractions = db.Column(db.Integer, default=0, nullable=False)
    average_productivity_rating = db.Column(db.Float, default=0.0, nullable=False)

    def to_dict(self, exclude=None):
        data = super().to_dict(exclude=exclude)
        if isinstance(self.summary_date, (date, datetime)):
            data["summary_date"] = self.summary_date.strftime("%Y-%m-%d")
        return data
