"""
LifeOS Automated Notification Dispatch Rule Engine
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Any
from backend.models.base import db
from backend.models.task import Task
from backend.services.notification_service import NotificationService


class NotificationRuleEngine:
    """
    Scans system events and dispatches automated reminder notifications.
    """

    @staticmethod
    def check_upcoming_task_deadlines(user_id: int) -> int:
        """Dispatches notifications for tasks due within the next 24 hours."""
        now = datetime.utcnow()
        cutoff = now + timedelta(hours=24)

        tasks = Task.query.filter(
            Task.user_id == user_id,
            Task.is_deleted == False,
            Task.status != "completed",
            Task.due_date >= now,
            Task.due_date <= cutoff
        ).all()

        dispatched = 0
        for t in tasks:
            NotificationService.create_notification(
                user_id=user_id,
                title=f"Task Due Soon: {t.title}",
                message=f"Task '{t.title}' is due within 24 hours.",
                notification_type="task_due",
                severity="warning",
                entity_type="task",
                entity_id=t.id
            )
            dispatched += 1

        return dispatched
