"""
LifeOS Extended Habit Analytics Domain Service Module 2
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
from backend.models.base import db
from backend.models.habit import Habit, HabitCompletion


class HabitAnalyticsServiceExt2:
    """
    Advanced habit streak retention, consistency metrics, and heatmap grid generator 2.
    """

    @staticmethod
    def compute_habit_streak_retention_2(user_id: int) -> Dict[str, Any]:
        """Computes longest active streaks and overall consistency factor."""
        habits = Habit.query.filter_by(user_id=user_id, is_deleted=False).all()
        if not habits:
            return {"active_habits_count": 0, "max_streak": 0, "avg_streak": 0.0}

        streaks = [h.current_streak for h in habits]
        max_s = max(streaks) if streaks else 0
        avg_s = round(sum(streaks) / len(streaks), 1) if streaks else 0.0

        return {
            "active_habits_count": len(habits),
            "max_streak": max_s,
            "avg_streak": avg_s,
            "habits_with_active_streaks": sum(1 for s in streaks if s > 0)
        }

    @staticmethod
    def generate_30_day_habit_matrix_2(user_id: int) -> List[Dict[str, Any]]:
        """Generates 30-day trailing habit completion matrix for heatmap UI rendering."""
        now = datetime.utcnow().date()
        matrix = []
        habits = Habit.query.filter_by(user_id=user_id, is_deleted=False).all()

        for d_offset in range(29, -1, -1):
            target_date = now - timedelta(days=d_offset)
            date_str = target_date.strftime("%Y-%m-%d")

            day_completions = 0
            for h in habits:
                if any(getattr(c, "completed_date", None) == target_date for c in getattr(h, "completions", [])):
                    day_completions += 1

            matrix.append({
                "date": date_str,
                "completed_count": day_completions,
                "total_habits": len(habits),
                "ratio": round(day_completions / max(len(habits), 1), 2)
            })

        return matrix
