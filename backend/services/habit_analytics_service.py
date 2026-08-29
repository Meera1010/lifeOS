"""
LifeOS Habit Tracker Advanced Analytics Domain Service
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Any
from sqlalchemy import func
from backend.models.base import db
from backend.models.habit import Habit, HabitCompletion
from backend.utilities.date_utils import get_last_n_days


class HabitAnalyticsService:
    """
    Provides deep-dive habit analytics:
    - Weekly consistency heatmaps
    - Streak retention ratios
    - Habit difficulty vs completion rate matrix
    """

    @staticmethod
    def get_streak_retention_summary(user_id: int) -> Dict[str, Any]:
        """Calculates habit streak retention metrics."""
        habits = Habit.query.filter_by(user_id=user_id, is_deleted=False).all()
        if not habits:
            return {"total_habits": 0, "active_streaks": 0, "retention_rate": 0.0}

        active = sum(1 for h in habits if h.current_streak > 0)
        retention = round((active / len(habits)) * 100.0, 1)

        return {
            "total_habits": len(habits),
            "active_streaks": active,
            "retention_rate": retention
        }
