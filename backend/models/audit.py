"""
LifeOS Audit Logging & System Analytics Models
"""

from datetime import datetime
from backend.models.base import db, TimestampMixin, SerializerMixin

class AuditLog(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    action = db.Column(db.String(100), nullable=False, index=True) # USER_LOGIN, TASK_CREATED, USER_DELETED, etc.
    resource_type = db.Column(db.String(50), nullable=False, index=True)
    resource_id = db.Column(db.String(50), nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def to_dict(self, exclude=None):
        data = super().to_dict(exclude=exclude)
        if isinstance(self.timestamp, datetime):
            data["timestamp"] = self.timestamp.isoformat()
        return data


class SystemMetric(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "system_metrics"

    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(100), nullable=False, index=True)
    metric_value = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(255), nullable=True)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
