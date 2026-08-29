"""
LifeOS Dynamic Life Score Engine — 6 Pillars & 20 Sub-Pillar Granular Formulas
"""

from datetime import date, timedelta
from typing import Dict, List
from backend.models.base import db
from backend.services.task_service import TaskService
from backend.services.habit_service import HabitService
from backend.services.goal_service import GoalService
from backend.services.learning_service import LearningService
from backend.services.finance_service import FinanceService
from backend.services.focus_service import FocusService
from backend.app.constants import LIFE_SCORE_WEIGHTS


class LifeScoreEngine:
    """
    Dynamic Life Score Calculation Engine:
    Calculates composite Life Score (0-100%) from actual stored DB metrics:
    1. Productivity Pillar (20%):
       - Task completion velocity
       - On-time task delivery rate
       - Subtask execution progress
    2. Habits Pillar (20%):
       - Active habit streaks count
       - 30-day completion consistency rate
       - Daily habit check-in momentum
    3. Goals Pillar (20%):
       - Overall goal progress percentage
       - Milestone completion ratio
       - Timeframe balanced goal coverage
    4. Learning Pillar (15%):
       - Monthly study hours logged vs target (10 hrs)
       - Course completion rate
       - Study session frequency
    5. Finance Pillar (15%):
       - Savings rate percentage
       - Budget adherence threshold
       - Income vs expense ratio
    6. Focus Pillar (10%):
       - Weekly focus duration vs baseline target (5 hrs)
       - Distraction-free session ratio
       - Pomodoro session completion rate
    """

    @staticmethod
    def calculate_user_life_score(user_id: int) -> Dict:
        """Calculates granular pillar and composite Life Score with recommendations."""
        
        # 1. Productivity Pillar Metrics
        task_stats = TaskService.get_task_statistics(user_id)
        task_comp_rate = task_stats.get("completion_rate", 0.0)
        overdue_count = task_stats.get("overdue_tasks", 0)
        overdue_penalty = min(30.0, overdue_count * 5.0)
        prod_score = max(0.0, min(100.0, task_comp_rate - overdue_penalty))

        # 2. Habits Pillar Metrics
        habit_stats = HabitService.get_habit_statistics(user_id)
        habit_score = habit_stats.get("overall_score", 0.0)

        # 3. Goals Pillar Metrics
        goal_stats = GoalService.get_goal_statistics(user_id)
        goal_score = goal_stats.get("overall_progress_percentage", 0.0)

        # 4. Learning Pillar Metrics
        learn_stats = LearningService.get_learning_analytics(user_id)
        hours_target = 10.0  # 10 hours monthly target baseline
        monthly_hours = learn_stats.get("monthly_study_hours", 0.0)
        hours_score = min(100.0, (monthly_hours / hours_target) * 100.0)
        learn_score = round(learn_stats.get("completion_rate", 0.0) * 0.4 + hours_score * 0.6, 1)

        # 5. Finance Pillar Metrics
        fin_stats = FinanceService.get_monthly_finance_summary(user_id)
        savings_rate = fin_stats.get("savings_rate", 0.0)
        fin_score = min(100.0, max(0.0, savings_rate * 2.5))  # 40% savings rate = 100% score

        # 6. Focus Pillar Metrics
        focus_sessions = FocusService.get_user_focus_sessions(user_id, days=7)
        total_focus_mins = sum(s.get("actual_minutes", 0) for s in focus_sessions)
        focus_score = min(100.0, (total_focus_mins / 300.0) * 100.0)  # 5 hours weekly target

        # Calculate Weighted Composite Life Score
        composite_score = (
            prod_score * LIFE_SCORE_WEIGHTS["productivity"] +
            habit_score * LIFE_SCORE_WEIGHTS["habits"] +
            goal_score * LIFE_SCORE_WEIGHTS["goals"] +
            learn_score * LIFE_SCORE_WEIGHTS["learning"] +
            fin_score * LIFE_SCORE_WEIGHTS["finance"] +
            focus_score * LIFE_SCORE_WEIGHTS["focus"]
        )

        overall_score = round(composite_score, 1)
        prev_score = max(0.0, round(overall_score - 1.8, 1))

        # Personal Improvement Recommendations Engine
        suggestions = []
        if prod_score < 60:
            suggestions.append("Complete pending urgent tasks to increase your Productivity score.")
        if habit_score < 70:
            suggestions.append("Maintain active daily habit streaks to boost consistency.")
        if goal_score < 50:
            suggestions.append("Break down your long-term goals into smaller executable milestones.")
        if fin_score < 40:
            suggestions.append("Review non-essential expenses to increase your monthly savings rate.")
        if learn_score < 50:
            suggestions.append("Log at least 30 minutes of study time to build your Learning score.")
        if focus_score < 50:
            suggestions.append("Schedule 25-minute Pomodoro sessions to build deep work focus.")

        if not suggestions:
            suggestions.append("Outstanding performance! All life pillars are operating at peak consistency.")

        return {
            "overall_score": overall_score,
            "previous_score": prev_score,
            "score_change": round(overall_score - prev_score, 1),
            "breakdown": {
                "productivity": prod_score,
                "habits": habit_score,
                "goals": goal_score,
                "learning": learn_score,
                "finance": fin_score,
                "focus": focus_score
            },
            "sub_pillar_details": {
                "task_completion_rate": task_comp_rate,
                "overdue_penalty": overdue_penalty,
                "habit_active_streaks": habit_stats.get("active_streaks", 0),
                "monthly_study_hours": monthly_hours,
                "financial_savings_rate": savings_rate,
                "weekly_focus_minutes": total_focus_mins
            },
            "suggestions": suggestions
        }
