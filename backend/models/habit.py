"""
LifeOS Habit Tracker Models
"""

from datetime import datetime, date
from backend.models.base import db, TimestampMixin, SoftDeleteMixin, SerializerMixin
from backend.app.constants import HabitFrequency

class Habit(db.Model, TimestampMixin, SoftDeleteMixin, SerializerMixin):
    __tablename__ = "habits"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default="General", nullable=False)
    color = db.Column(db.String(20), default="#10b981", nullable=False)
    icon = db.Column(db.String(50), default="check-circle", nullable=False)
    frequency = db.Column(db.String(20), default=HabitFrequency.DAILY.value, nullable=False)
    target_days_per_week = db.Column(db.Integer, default=7, nullable=False)
    target_value = db.Column(db.Float, default=1.0, nullable=False) # e.g. 8 glasses of water, 30 mins
    unit = db.Column(db.String(30), default="times", nullable=False)
    
    current_streak = db.Column(db.Integer, default=0, nullable=False)
    best_streak = db.Column(db.Integer, default=0, nullable=False)
    total_completions = db.Column(db.Integer, default=0, nullable=False)
    archived = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    completions = db.relationship("HabitCompletion", backref="habit", cascade="all, delete-orphan", lazy="dynamic")
    reminders = db.relationship("HabitReminder", backref="habit", cascade="all, delete-orphan", lazy="dynamic")

    def update_streak_counts(self):
        """Calculates current streak and best streak dynamically based on completion history."""
        completions_list = self.completions.filter_by(status="completed").order_by(HabitCompletion.completion_date.desc()).all()
        if not completions_list:
            self.current_streak = 0
            db.session.add(self)
            return

        dates = sorted(set(c.completion_date for c in completions_list), reverse=True)
        today = date.today()
        
        streak = 0
        expected_date = today
        
        # Check if completed today or yesterday to preserve active streak
        if dates[0] == today:
            expected_date = today
        elif (today - dates[0]).days == 1:
            expected_date = dates[0]
        else:
            self.current_streak = 0
            db.session.add(self)
            return

        for d in dates:
            if (expected_date - d).days == 0:
                streak += 1
                from datetime import timedelta
                expected_date = d - timedelta(days=1)
            elif (expected_date - d).days > 0:
                break

        self.current_streak = streak
        if self.current_streak > self.best_streak:
            self.best_streak = self.current_streak
        self.total_completions = len(completions_list)
        db.session.add(self)

    def to_dict(self, exclude=None, include_relationships=True):
        data = super().to_dict(exclude=exclude)
        if include_relationships:
            # Include recent 30 completions
            recent = self.completions.order_by(HabitCompletion.completion_date.desc()).limit(30).all()
            data["recent_completions"] = [c.to_dict() for c in recent]
        return data


class HabitCompletion(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "habit_completions"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    completion_date = db.Column(db.Date, nullable=False, index=True)
    value = db.Column(db.Float, default=1.0, nullable=False)
    status = db.Column(db.String(20), default="completed", nullable=False) # completed, skipped, missed
    notes = db.Column(db.String(255), nullable=True)

    def to_dict(self, exclude=None):
        data = super().to_dict(exclude=exclude)
        if isinstance(self.completion_date, (date, datetime)):
            data["completion_date"] = self.completion_date.strftime("%Y-%m-%d")
        return data


class HabitStreakHistory(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "habit_streak_histories"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    streak_count = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)


class HabitReminder(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "habit_reminders"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    reminder_time = db.Column(db.String(10), nullable=False) # e.g. "08:00"
    days_of_week = db.Column(db.String(50), default="0,1,2,3,4,5,6", nullable=False) # CSV 0=Mon, 6=Sun
    is_enabled = db.Column(db.Boolean, default=True, nullable=False)
