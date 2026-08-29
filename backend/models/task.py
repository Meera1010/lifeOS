"""
LifeOS Task Manager Models
"""

from datetime import datetime
from backend.models.base import db, TimestampMixin, SoftDeleteMixin, SerializerMixin
from backend.app.constants import PriorityLevel, TaskStatus

task_tags_table = db.Table(
    "task_tags_mapping",
    db.Column("task_id", db.Integer, db.ForeignKey("tasks.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("task_tags.id"), primary_key=True)
)

class TaskCategory(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "task_categories"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(20), default="#4f46e5", nullable=False)
    icon = db.Column(db.String(50), default="folder", nullable=False)
    description = db.Column(db.String(255), nullable=True)

    tasks = db.relationship("Task", backref="category", lazy="dynamic")


class TaskTag(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "task_tags"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), default="#64748b", nullable=False)


class Task(db.Model, TimestampMixin, SoftDeleteMixin, SerializerMixin):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("task_categories.id"), nullable=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default=PriorityLevel.MEDIUM.value, nullable=False, index=True)
    status = db.Column(db.String(20), default=TaskStatus.PENDING.value, nullable=False, index=True)
    due_date = db.Column(db.DateTime, nullable=True, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    estimated_minutes = db.Column(db.Integer, default=0, nullable=False)
    actual_minutes = db.Column(db.Integer, default=0, nullable=False)
    
    # Recurrence Settings
    is_recurring = db.Column(db.Boolean, default=False, nullable=False)
    recurrence_pattern = db.Column(db.String(50), nullable=True) # daily, weekly, monthly, custom
    recurrence_interval = db.Column(db.Integer, default=1, nullable=False)
    recurrence_end_date = db.Column(db.DateTime, nullable=True)

    # Relationships
    subtasks = db.relationship("Subtask", backref="task", cascade="all, delete-orphan", lazy="joined")
    tags = db.relationship("TaskTag", secondary=task_tags_table, backref=db.backref("tasks", lazy="dynamic"))
    activity_logs = db.relationship("TaskActivityLog", backref="task", cascade="all, delete-orphan", lazy="dynamic")

    def mark_completed(self):
        self.status = TaskStatus.COMPLETED.value
        self.completed_at = datetime.utcnow()
        db.session.add(self)

    def mark_pending(self):
        self.status = TaskStatus.PENDING.value
        self.completed_at = None
        db.session.add(self)

    def get_progress_percentage(self):
        total_subtasks = len(self.subtasks)
        if total_subtasks == 0:
            return 100.0 if self.status == TaskStatus.COMPLETED.value else 0.0
        completed = sum(1 for st in self.subtasks if st.is_completed)
        return round((completed / total_subtasks) * 100.0, 1)

    def to_dict(self, exclude=None, include_relationships=True):
        data = super().to_dict(exclude=exclude)
        data["progress_percentage"] = self.get_progress_percentage()
        if include_relationships:
            data["subtasks"] = [st.to_dict() for st in self.subtasks]
            data["tags"] = [tg.to_dict() for tg in self.tags]
            if self.category:
                data["category"] = self.category.to_dict()
        return data


class Subtask(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "subtasks"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    order_index = db.Column(db.Integer, default=0, nullable=False)

    def toggle_completion(self):
        self.is_completed = not self.is_completed
        self.completed_at = datetime.utcnow() if self.is_completed else None
        db.session.add(self)


class TaskActivityLog(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "task_activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(50), nullable=False) # created, updated, status_changed, subtask_added, deleted
    details = db.Column(db.Text, nullable=True)
