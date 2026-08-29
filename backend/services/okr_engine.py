"""
LifeOS OKR (Objectives and Key Results) Alignment Engine
"""

from typing import Dict, List
from backend.services.goal_service import GoalService

class OKREngine:

    @staticmethod
    def calculate_okr_alignment(user_id: int) -> Dict:
        """
        Computes Objective alignment across all active goals:
        - Key Results Progress %
        - Alignment Score Index
        - Objective Completion Velocity
        """
        goals = GoalService.get_user_goals(user_id)
        if not goals:
            return {"total_objectives": 0, "overall_alignment_score": 0.0, "objectives": []}

        objectives = []
        total_score = 0.0

        for g in goals:
            milestones = g.get("milestones", [])
            total_kr = len(milestones)
            completed_kr = sum(1 for m in milestones if m.get("is_completed"))
            kr_score = round((completed_kr / total_kr) * 100.0, 1) if total_kr > 0 else g.get("progress_percentage", 0.0)

            objectives.append({
                "goal_id": g["id"],
                "objective_title": g["title"],
                "category": g["category"],
                "key_results_total": total_kr,
                "key_results_completed": completed_kr,
                "progress_percentage": kr_score
            })
            total_score += kr_score

        overall = round(total_score / len(goals), 1)

        return {
            "total_objectives": len(goals),
            "overall_alignment_score": overall,
            "objectives": objectives
        }
