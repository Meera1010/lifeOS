"""
LifeOS Calendar & Event Models
"""

from datetime import datetime
from backend.models.base import db, TimestampMixin, SoftDeleteMixin, SerializerMixin

class EventCategory(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "event_categories"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(20), default="#3b82f6", nullable=False)
    icon = db.Column(db.String(50), default="calendar", nullable=False)


class CalendarEvent(db.Model, TimestampMixin, SoftDeleteMixin, SerializerMixin):
    __tablename__ = "calendar_events"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("event_categories.id"), nullable=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, nullable=False, index=True)
    is_all_day = db.Column(db.Boolean, default=False, nullable=False)
    
    # Recurrence Settings
    is_recurring = db.Column(db.Boolean, default=False, nullable=False)
    recurrence_rule = db.Column(db.String(100), nullable=True) # FREQ=DAILY;INTERVAL=1
    
    # Color & Icon override
    color = db.Column(db.String(20), default="#3b82f6", nullable=False)
    
    # Linked domain entities (optional foreign keys for unified view)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"), nullable=True)

    reminders = db.relationship("EventReminder", backref="event", cascade="all, delete-orphan", lazy="joined")

    def to_dict(self, exclude=None, include_relationships=True):
        data = super().to_dict(exclude=exclude)
        if include_relationships:
            data["reminders"] = [r.to_dict() for r in self.reminders]
            if self.category_id:
                cat = EventCategory.query.get(self.category_id)
                if cat:
                    data["category"] = cat.to_dict()
        return data


class EventReminder(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "event_reminders"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("calendar_events.id"), nullable=False)
    minutes_before = db.Column(db.Integer, default=15, nullable=False) # 15 mins before
    notification_type = db.Column(db.String(30), default="in_app", nullable=False) # in_app, email
    is_sent = db.Column(db.Boolean, default=False, nullable=False)
