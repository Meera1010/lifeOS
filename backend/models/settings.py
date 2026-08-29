"""
LifeOS User Settings & Preference Models
"""

from backend.models.base import db, TimestampMixin, SerializerMixin

class UserSettings(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "user_settings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    theme = db.Column(db.String(20), default="dark", nullable=False) # dark, light, system, cyber
    accent_color = db.Column(db.String(20), default="#4f46e5", nullable=False)
    time_format = db.Column(db.String(10), default="12h", nullable=False) # 12h, 24h
    date_format = db.Column(db.String(20), default="YYYY-MM-DD", nullable=False)
    start_day_of_week = db.Column(db.Integer, default=1, nullable=False) # 0=Sunday, 1=Monday
    currency_symbol = db.Column(db.String(10), default="$", nullable=False)
    default_landing_page = db.Column(db.String(50), default="dashboard", nullable=False)
    
    # Privacy
    is_profile_public = db.Column(db.Boolean, default=False, nullable=False)
    show_activity_status = db.Column(db.Boolean, default=True, nullable=False)
    compact_mode = db.Column(db.Boolean, default=False, nullable=False)


class DashboardPreference(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "dashboard_preferences"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    visible_widgets = db.Column(db.Text, default="tasks,habits,goals,finance,health,learning,productivity_chart,recent_activity", nullable=False)
    widget_order = db.Column(db.Text, default="tasks,habits,goals,finance,learning,productivity_chart", nullable=False)
    quick_links = db.Column(db.Text, default="task_new,habit_checkin,focus_start,transaction_new", nullable=False)
