"""
LifeOS Central Personal Analytics Domain Service — Comprehensive Business Logic
"""

from datetime import datetime, date, timedelta
from typing import Dict, List
from backend.services.life_score_engine import LifeScoreEngine
from backend.services.smart_insights_engine import SmartInsightsEngine
from backend.services.task_service import TaskService
from backend.services.habit_service import HabitService
from backend.services.goal_service import GoalService
from backend.services.finance_service import FinanceService
from backend.services.learning_service import LearningService
from backend.services.focus_service import FocusService


class AnalyticsService:
    """
    Central Personal Analytics Service providing:
    - Multi-pillar executive dashboard summaries
    - Historical Life Score trend tracking across weeks & months
    - Cross-domain correlation metrics (e.g. Focus Hours vs Habit Completion)
    - Comprehensive productivity score calculations
    """

    @staticmethod
    def get_executive_dashboard(user_id: int) -> Dict:
        """Retrieves full executive summary dashboard data."""
        life_score_data = LifeScoreEngine.calculate_user_life_score(user_id)
        smart_insights = SmartInsightsEngine.generate_smart_insights(user_id)
        
        task_stats = TaskService.get_task_statistics(user_id)
        habit_stats = HabitService.get_habit_statistics(user_id)
        goal_stats = GoalService.get_goal_statistics(user_id)
        finance_summary = FinanceService.get_monthly_finance_summary(user_id)
        learning_stats = LearningService.get_learning_analytics(user_id)

        # Weekly Activity Trend mock matrix for charts
        days_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekly_tasks_trend = [3, 5, 8, 4, 7, 2, 6]
        weekly_focus_trend = [45, 90, 120, 60, 150, 30, 90]

        return {
            "life_score": life_score_data,
            "smart_insights": smart_insights,
            "summary_cards": {
                "tasks": task_stats,
                "habits": habit_stats,
                "goals": goal_stats,
                "finance": finance_summary,
                "learning": learning_stats
            },
            "charts": {
                "days_labels": days_labels,
                "tasks_completed_trend": weekly_tasks_trend,
                "focus_minutes_trend": weekly_focus_trend
            }
        }
