"""
LifeOS Task Manager Advanced Analytics Domain Service
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Any
from sqlalchemy import func, desc, asc
from backend.models.base import db
from backend.models.task import Task, TaskCategory, TaskActivityLog
from backend.utilities.date_utils import get_last_n_days, get_month_range, get_week_range


class TaskAnalyticsService:
    """
    Provides deep-dive task analytics:
    - Daily velocity completion trends
    - Category distribution ratios
    - Priority backlog health indicators
    - Overdue task aging calculations
    """

    @staticmethod
    def get_task_velocity_trend(user_id: int, days: int = 14) -> Dict[str, Any]:
        """Calculates daily completed task count over past N days."""
        days_list = get_last_n_days(days)
        formatted_dates = [d.strftime("%Y-%m-%d") for d in days_list]

        daily_counts = {}
        for d in days_list:
            start_dt = datetime.combine(d, datetime.min.time())
            end_dt = datetime.combine(d, datetime.max.time())
            
            count = Task.query.filter(
                Task.user_id == user_id,
                Task.is_deleted == False,
                Task.status == "completed",
                Task.completed_at >= start_dt,
                Task.completed_at <= end_dt
            ).count()
            daily_counts[d.strftime("%Y-%m-%d")] = count

        return {
            "period_days": days,
            "dates": formatted_dates,
            "velocity_counts": [daily_counts[d] for d in formatted_dates]
        }

    @staticmethod
    def get_category_distribution(user_id: int) -> List[Dict[str, Any]]:
        """Calculates task count distribution across categories."""
        results = db.session.query(
            TaskCategory.name,
            TaskCategory.color,
            func.count(Task.id).label("task_count")
        ).join(Task, Task.category_id == TaskCategory.id).filter(
            Task.user_id == user_id,
            Task.is_deleted == False
        ).group_by(TaskCategory.id).all()

        total = sum(r[2] for r in results) or 1
        return [
            {
                "category_name": r[0],
                "color": r[1],
                "task_count": r[2],
                "percentage": round((r[2] / total) * 100.0, 1)
            }
            for r in results
        ]
