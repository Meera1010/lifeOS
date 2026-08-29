"""
LifeOS Smart Insights Rule Engine — Behavioral Pattern Recognition
"""

from typing import List, Dict
from backend.services.task_service import TaskService
from backend.services.habit_service import HabitService
from backend.services.finance_service import FinanceService
from backend.services.focus_service import FocusService


class SmartInsightsEngine:
    """
    Rule-Based Behavioral Analytics & Smart Insights Engine:
    Analyzes historical stored user activity patterns across multiple domains and
    generates contextual actionable insights.
    """

    @staticmethod
    def generate_smart_insights(user_id: int) -> List[Dict]:
        """Scans database patterns and builds array of insight cards."""
        insights = []

        # 1. Overdue Task Pattern Rule
        task_stats = TaskService.get_task_statistics(user_id)
        if task_stats.get("overdue_tasks", 0) > 0:
            insights.append({
                "type": "warning",
                "title": "Overdue Task Backlog",
                "message": f"You have {task_stats['overdue_tasks']} overdue tasks pending. Reschedule or complete them to avoid productivity fatigue.",
                "action_url": "#tasks?status=pending",
                "category": "Tasks"
            })

        # 2. Habit Streak Momentum Rule
        habit_stats = HabitService.get_habit_statistics(user_id)
        if habit_stats.get("longest_streak", 0) >= 7:
            insights.append({
                "type": "success",
                "title": "Habit Streak Momentum",
                "message": f"Great job! Your longest active habit streak has reached {habit_stats['longest_streak']} consecutive days.",
                "action_url": "#habits",
                "category": "Habits"
            })

        # 3. High Savings Rate Rule
        fin_stats = FinanceService.get_monthly_finance_summary(user_id)
        if fin_stats.get("savings_rate", 0.0) >= 30.0:
            insights.append({
                "type": "info",
                "title": "Strong Savings Rate",
                "message": f"Your current monthly savings rate is {fin_stats['savings_rate']}%, well above the 20% benchmark target.",
                "action_url": "#finance",
                "category": "Finance"
            })
        elif fin_stats.get("total_expenses", 0.0) > fin_stats.get("total_income", 0.0) and fin_stats.get("total_income", 0.0) > 0:
            insights.append({
                "type": "danger",
                "title": "Monthly Spending Exceeds Income",
                "message": f"Monthly expenses (${fin_stats['total_expenses']}) currently exceed income (${fin_stats['total_income']}). Review your spending categories.",
                "action_url": "#finance",
                "category": "Finance"
            })

        # 4. Deep Work Focus Rule
        focus_sessions = FocusService.get_user_focus_sessions(user_id, days=7)
        total_distractions = sum(s.get("distraction_count", 0) for s in focus_sessions)
        if total_distractions > 5:
            insights.append({
                "type": "warning",
                "title": "Frequent Focus Interruptions",
                "message": f"Logged {total_distractions} distractions during recent focus sessions. Consider enabling notification blocker.",
                "action_url": "#focus",
                "category": "Focus"
            })

        # Default fallback insight if clean slate
        if not insights:
            insights.append({
                "type": "info",
                "title": "Welcome to LifeOS Analytics",
                "message": "As you log tasks, habits, financial transactions, and focus sessions, Smart Insights will automatically highlight behavioral optimizations.",
                "action_url": "#dashboard",
                "category": "General"
            })

        return insights

    generate_user_insights = generate_smart_insights
