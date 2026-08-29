"""
LifeOS Extended Task Analytics Domain Service Module 4
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
from backend.models.base import db
from backend.models.task import Task, Subtask


class TaskAnalyticsServiceExt4:
    """
    Advanced task analytics, velocity estimation, and breakdown calculations module 4.
    """

    @staticmethod
    def calculate_task_completion_velocity_4(user_id: int, days: int = 30) -> Dict[str, Any]:
        """Calculates completed task velocity over specified trailing days."""
        now = datetime.utcnow()
        since = now - timedelta(days=days)

        tasks = Task.query.filter(
            Task.user_id == user_id,
            Task.is_deleted == False,
            Task.updated_at >= since
        ).all()

        total = len(tasks)
        completed = [t for t in tasks if t.status == "completed"]
        completed_count = len(completed)

        velocity_per_day = round(completed_count / max(days, 1), 2)
        completion_ratio = round((completed_count / total * 100.0), 1) if total > 0 else 0.0

        return {
            "user_id": user_id,
            "period_days": days,
            "total_tasks_tracked": total,
            "completed_tasks_count": completed_count,
            "daily_velocity": velocity_per_day,
            "completion_ratio_pct": completion_ratio
        }

    @staticmethod
    def analyze_task_priority_distribution_4(user_id: int) -> Dict[str, int]:
        """Analyzes active task count grouped by priority tier."""
        tasks = Task.query.filter_by(user_id=user_id, is_deleted=False).all()
        counts = {"high": 0, "medium": 0, "low": 0}
        for t in tasks:
            p = (t.priority or "medium").lower()
            if p in counts:
                counts[p] += 1
            else:
                counts["medium"] += 1
        return counts

    @staticmethod
    def get_subtask_hierarchy_depth_4(user_id: int) -> Dict[str, Any]:
        """Computes subtask hierarchy completion statistics."""
        tasks = Task.query.filter_by(user_id=user_id, is_deleted=False).all()
        total_subtasks = 0
        completed_subtasks = 0
        for t in tasks:
            subtasks = getattr(t, "subtasks", [])
            total_subtasks += len(subtasks)
            completed_subtasks += sum(1 for st in subtasks if getattr(st, "is_completed", False))

        return {
            "total_subtasks": total_subtasks,
            "completed_subtasks": completed_subtasks,
            "subtask_completion_pct": round(completed_subtasks / max(total_subtasks, 1) * 100.0, 1)
        }
