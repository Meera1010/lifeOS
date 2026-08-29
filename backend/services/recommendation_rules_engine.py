"""
LifeOS Personal Recommendation Rules Engine
"""

from typing import List, Dict, Any
from backend.services.life_score_engine import LifeScoreEngine


class RecommendationRulesEngine:
    """
    Rule-based recommendation engine delivering actionable advice
    based on Life Score pillar breakdowns.
    """

    @staticmethod
    def generate_personalized_recommendations(user_id: int) -> List[Dict[str, Any]]:
        """Scans user metrics and returns prioritized recommendation cards."""
        life_score = LifeScoreEngine.calculate_user_life_score(user_id)
        breakdown = life_score.get("breakdown", {})

        recommendations = []

        if breakdown.get("productivity", 0) < 60:
            recommendations.append({
                "pillar": "Productivity",
                "priority": "High",
                "title": "Clear Overdue Tasks",
                "description": "Your productivity pillar is below optimal threshold. Complete or reschedule overdue tasks.",
                "action_link": "#tasks?status=pending"
            })

        if breakdown.get("finance", 0) < 50:
            recommendations.append({
                "pillar": "Finance",
                "priority": "High",
                "title": "Increase Savings Rate",
                "description": "Your current savings rate is below target. Set up budget limits to reduce discretionary spending.",
                "action_link": "#finance"
            })

        if breakdown.get("focus", 0) < 50:
            recommendations.append({
                "pillar": "Focus",
                "priority": "Medium",
                "title": "Schedule Daily Pomodoro Sessions",
                "description": "Boost your deep work focus score by logging 25-minute distraction-free focus sessions.",
                "action_link": "#focus"
            })

        return recommendations
