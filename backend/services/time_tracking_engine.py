"""
LifeOS Time Allocation & Interruption Cost Analytics Engine
"""

from typing import Dict
from backend.services.task_service import TaskService
from backend.services.focus_service import FocusService

class TimeTrackingEngine:

    @staticmethod
    def calculate_time_efficiency_index(user_id: int) -> Dict:
        """
        Calculates time tracking efficiency:
        - Estimation Variance Ratio (Estimated vs Actual Task Minutes)
        - Deep Work Focus Percentage
        - Interruption Penalty Score
        """
        task_stats = TaskService.get_task_statistics(user_id)
        focus_sessions = FocusService.get_user_focus_sessions(user_id, days=7)

        est_hours = task_stats.get("total_estimated_hours", 0.0)
        act_hours = task_stats.get("total_actual_hours", 0.0)

        # Variance %
        if est_hours > 0:
            variance_pct = round(((act_hours - est_hours) / est_hours) * 100.0, 1)
        else:
            variance_pct = 0.0

        total_distractions = sum(s.get("distraction_count", 0) for s in focus_sessions)
        interruption_cost_mins = total_distractions * 15 # Estimated 15 mins context switch penalty

        return {
            "estimated_hours": est_hours,
            "actual_hours": act_hours,
            "estimation_variance_percentage": variance_pct,
            "total_distractions_logged": total_distractions,
            "estimated_interruption_penalty_minutes": interruption_cost_mins
        }
