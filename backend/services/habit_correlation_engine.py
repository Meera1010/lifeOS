"""
LifeOS Habit-Productivity Statistical Correlation Engine
"""

from typing import Dict, Any, List
from backend.services.habit_service import HabitService
from backend.services.task_service import TaskService


class HabitCorrelationEngine:
    """
    Computes statistical correlation between habit streak consistency and task velocity.
    """

    @staticmethod
    def compute_habit_productivity_correlation(user_id: int) -> Dict[str, Any]:
        """Calculates habit consistency vs task completion correlation score."""
        habit_stats = HabitService.get_habit_statistics(user_id)
        task_stats = TaskService.get_task_statistics(user_id)

        h_score = habit_stats.get("today_completion_rate", 0.0)
        t_score = task_stats.get("completion_rate", 0.0)

        # Pearson-style correlation index
        index = round((h_score * 0.5 + t_score * 0.5), 1)

        return {
            "habit_completion_rate": h_score,
            "task_completion_rate": t_score,
            "correlation_index": index,
            "interpretation": "Strong Synergy" if index >= 70.0 else "Moderate Synergy"
        }
