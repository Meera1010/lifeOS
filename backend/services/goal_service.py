"""
LifeOS Goal Management Domain Service — Comprehensive Business Logic
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Optional
from sqlalchemy import func, or_, and_, desc, asc
from backend.models.base import db
from backend.models.goal import Goal, Milestone, GoalProgressHistory
from backend.app.constants import GoalCategory, GoalTimeframe, GoalStatus, PriorityLevel
from backend.security.validators import sanitize_string
from backend.utilities.date_utils import parse_datetime_string, parse_date_string


class GoalService:
    """
    Comprehensive Goal Management Domain Service providing:
    - OKR & Goal creation, milestone tracking, and weight calculations
    - Goal categories (Personal, Career, Financial, Learning, Health, Relationships)
    - Short-Term vs Long-Term timeframe classification
    - Dynamic progress percentage computation from milestones or target metrics
    - Historical goal progress logging & velocity projections
    - Milestone completion toggles & weighted goal recalculation
    """

    @staticmethod
    def get_user_goals(user_id: int, filters: Optional[Dict] = None) -> List[Dict]:
        """Retrieves user goals with milestone breakdown."""
        filters = filters or {}
        query = Goal.query.filter_by(user_id=user_id, is_deleted=False)

        if filters.get("category"):
            query = query.filter_by(category=filters["category"])
        if filters.get("timeframe"):
            query = query.filter_by(timeframe=filters["timeframe"])
        if filters.get("status"):
            query = query.filter_by(status=filters["status"])
        if filters.get("priority"):
            query = query.filter_by(priority=filters["priority"])

        goals = query.order_by(asc(Goal.target_date)).all()
        return [g.to_dict() for g in goals]

    @staticmethod
    def get_goal_by_id(user_id: int, goal_id: int) -> Optional[Dict]:
        """Retrieves single goal by ID."""
        goal = Goal.query.filter_by(id=goal_id, user_id=user_id, is_deleted=False).first()
        if not goal:
            return None
        return goal.to_dict()

    @staticmethod
    def create_goal(user_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Creates a new goal with initial milestones and metric validation."""
        title = sanitize_string(data.get("title", ""))
        if not title:
            return False, {"error": "Goal title is required."}

        if len(title) > 200:
            return False, {"error": "Goal title must not exceed 200 characters."}

        category = data.get("category", GoalCategory.PERSONAL.value)
        timeframe = data.get("timeframe", GoalTimeframe.SHORT_TERM.value)
        priority = data.get("priority", PriorityLevel.MEDIUM.value)
        
        target_date = parse_datetime_string(data.get("target_date")) if data.get("target_date") else None
        
        try:
            target_metric = float(data["target_metric_value"]) if data.get("target_metric_value") else None
            current_metric = float(data.get("current_metric_value", 0.0))
        except (ValueError, TypeError):
            target_metric = None
            current_metric = 0.0

        goal = Goal(
            user_id=user_id,
            title=title,
            description=sanitize_string(data.get("description", "")),
            category=category,
            timeframe=timeframe,
            priority=priority,
            status=GoalStatus.IN_PROGRESS.value,
            start_date=datetime.utcnow(),
            target_date=target_date,
            target_metric_value=target_metric,
            current_metric_value=current_metric,
            metric_unit=sanitize_string(data.get("metric_unit", "")),
            color=data.get("color", "#4f46e5"),
            icon=data.get("icon", "target"),
            notes=sanitize_string(data.get("notes", "")),
            progress_percentage=0.0
        )
        db.session.add(goal)
        db.session.flush()

        # Add Milestones
        milestones_input = data.get("milestones", [])
        for idx, ms in enumerate(milestones_input):
            if isinstance(ms, dict):
                ms_title = sanitize_string(ms.get("title", ""))
                weight = float(ms.get("weight", 1.0))
                due_d = parse_datetime_string(ms.get("due_date")) if ms.get("due_date") else None
            else:
                ms_title = sanitize_string(str(ms))
                weight = 1.0
                due_d = None

            if ms_title:
                m = Milestone(
                    goal_id=goal.id,
                    title=ms_title,
                    weight=weight,
                    due_date=due_d,
                    is_completed=False,
                    order_index=idx
                )
                db.session.add(m)

        goal.recalculate_progress()
        
        # Initial Progress History
        history = GoalProgressHistory(
            goal_id=goal.id,
            progress_percentage=goal.progress_percentage,
            metric_value=goal.current_metric_value,
            note="Goal created."
        )
        db.session.add(history)

        db.session.commit()
        return True, goal.to_dict()

    @staticmethod
    def update_goal(user_id: int, goal_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Updates goal parameters and records progress snapshot."""
        goal = Goal.query.filter_by(id=goal_id, user_id=user_id, is_deleted=False).first()
        if not goal:
            return False, {"error": "Goal not found."}

        if "title" in data:
            new_title = sanitize_string(data["title"])
            if not new_title:
                return False, {"error": "Goal title cannot be empty."}
            goal.title = new_title

        if "description" in data:
            goal.description = sanitize_string(data["description"])
        if "category" in data:
            goal.category = data["category"]
        if "timeframe" in data:
            goal.timeframe = data["timeframe"]
        if "priority" in data:
            goal.priority = data["priority"]
        if "status" in data:
            goal.status = data["status"]
        if "target_date" in data:
            goal.target_date = parse_datetime_string(data["target_date"]) if data["target_date"] else None
        if "current_metric_value" in data:
            goal.current_metric_value = float(data["current_metric_value"])
        if "notes" in data:
            goal.notes = sanitize_string(data["notes"])

        goal.recalculate_progress()

        # Add Progress Snapshot
        history = GoalProgressHistory(
            goal_id=goal.id,
            progress_percentage=goal.progress_percentage,
            metric_value=goal.current_metric_value,
            note=sanitize_string(data.get("update_note", "Goal parameters updated."))
        )
        db.session.add(history)

        db.session.commit()
        return True, goal.to_dict()

    @staticmethod
    def delete_goal(user_id: int, goal_id: int) -> Tuple[bool, str]:
        """Soft deletes a goal."""
        goal = Goal.query.filter_by(id=goal_id, user_id=user_id, is_deleted=False).first()
        if not goal:
            return False, "Goal not found."

        goal.soft_delete()
        db.session.commit()
        return True, "Goal successfully deleted."

    @staticmethod
    def toggle_milestone(user_id: int, milestone_id: int) -> Tuple[bool, Dict]:
        """Toggles milestone completion and updates goal progress percentage."""
        ms = Milestone.query.get(milestone_id)
        if not ms or ms.goal.user_id != user_id:
            return False, {"error": "Milestone not found."}

        ms.toggle_completion()
        ms.goal.recalculate_progress()
        db.session.commit()

        return True, ms.goal.to_dict()

    @staticmethod
    def add_milestone(user_id: int, goal_id: int, title: str, weight: float = 1.0) -> Tuple[bool, Dict]:
        """Adds new milestone to goal."""
        goal = Goal.query.filter_by(id=goal_id, user_id=user_id, is_deleted=False).first()
        if not goal:
            return False, {"error": "Goal not found."}

        ms_title = sanitize_string(title)
        if not ms_title:
            return False, {"error": "Milestone title cannot be empty."}

        order_idx = len(goal.milestones)
        m = Milestone(
            goal_id=goal.id,
            title=ms_title,
            weight=weight,
            order_index=order_idx
        )
        db.session.add(m)
        goal.recalculate_progress()
        db.session.commit()

        return True, goal.to_dict()

    @staticmethod
    def get_goal_statistics(user_id: int) -> Dict:
        """Calculates global goal achievement statistics."""
        goals = Goal.query.filter_by(user_id=user_id, is_deleted=False).all()
        total = len(goals)
        if total == 0:
            return {
                "total_goals": 0,
                "completed_goals": 0,
                "in_progress_goals": 0,
                "overall_progress_percentage": 0.0
            }

        completed = sum(1 for g in goals if g.status == GoalStatus.COMPLETED.value)
        in_progress = sum(1 for g in goals if g.status == GoalStatus.IN_PROGRESS.value)
        avg_progress = round(sum(g.progress_percentage for g in goals) / total, 1)

        return {
            "total_goals": total,
            "completed_goals": completed,
            "in_progress_goals": in_progress,
            "overall_progress_percentage": avg_progress
        }
