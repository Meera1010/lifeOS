"""
LifeOS Goal Management Models
"""

from datetime import datetime
from backend.models.base import db, TimestampMixin, SoftDeleteMixin, SerializerMixin
from backend.app.constants import GoalCategory, GoalTimeframe, GoalStatus, PriorityLevel

class Goal(db.Model, TimestampMixin, SoftDeleteMixin, SerializerMixin):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default=GoalCategory.PERSONAL.value, nullable=False, index=True)
    timeframe = db.Column(db.String(30), default=GoalTimeframe.SHORT_TERM.value, nullable=False, index=True)
    priority = db.Column(db.String(20), default=PriorityLevel.MEDIUM.value, nullable=False)
    status = db.Column(db.String(20), default=GoalStatus.IN_PROGRESS.value, nullable=False, index=True)
    
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    target_date = db.Column(db.DateTime, nullable=True, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    progress_percentage = db.Column(db.Float, default=0.0, nullable=False)
    target_metric_value = db.Column(db.Float, nullable=True) # e.g. $10,000 saved, 50 books read
    current_metric_value = db.Column(db.Float, default=0.0, nullable=True)
    metric_unit = db.Column(db.String(30), nullable=True)
    
    color = db.Column(db.String(20), default="#4f46e5", nullable=False)
    icon = db.Column(db.String(50), default="target", nullable=False)
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    milestones = db.relationship("Milestone", backref="goal", cascade="all, delete-orphan", lazy="joined")
    history = db.relationship("GoalProgressHistory", backref="goal", cascade="all, delete-orphan", lazy="dynamic")

    def recalculate_progress(self):
        """Calculates goal progress from milestones or raw metric value."""
        if self.target_metric_value and self.target_metric_value > 0:
            val = min(100.0, (self.current_metric_value / self.target_metric_value) * 100.0)
            self.progress_percentage = round(val, 1)
        elif self.milestones:
            total = len(self.milestones)
            completed = sum(1 for m in self.milestones if m.is_completed)
            self.progress_percentage = round((completed / total) * 100.0, 1)
        
        if self.progress_percentage >= 100.0 and self.status != GoalStatus.COMPLETED.value:
            self.status = GoalStatus.COMPLETED.value
            self.completed_at = datetime.utcnow()
        elif self.progress_percentage < 100.0 and self.status == GoalStatus.COMPLETED.value:
            self.status = GoalStatus.IN_PROGRESS.value
            self.completed_at = None

        db.session.add(self)

    def to_dict(self, exclude=None, include_relationships=True):
        data = super().to_dict(exclude=exclude)
        if include_relationships:
            data["milestones"] = [m.to_dict() for m in self.milestones]
        return data


class Milestone(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "milestones"

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    weight = db.Column(db.Float, default=1.0, nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)

    def toggle_completion(self):
        self.is_completed = not self.is_completed
        self.completed_at = datetime.utcnow() if self.is_completed else None
        db.session.add(self)


class GoalProgressHistory(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "goal_progress_histories"

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"), nullable=False, index=True)
    progress_percentage = db.Column(db.Float, nullable=False)
    metric_value = db.Column(db.Float, nullable=True)
    note = db.Column(db.String(255), nullable=True)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
