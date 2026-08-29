"""
LifeOS Data Integrity & Consistency Audit Service
"""

from typing import Dict, Any
from backend.models.base import db
from backend.models.task import Task
from backend.models.habit import Habit
from backend.models.goal import Goal


class DataIntegrityService:
    """
    Audits database constraints, orphaned records, and referential integrity.
    """

    @staticmethod
    def run_integrity_audit() -> Dict[str, Any]:
        """Scans database models for consistency anomalies."""
        orphaned_subtasks = db.session.execute("SELECT count(*) FROM task_subtasks WHERE task_id NOT IN (SELECT id FROM tasks)").scalar() or 0
        orphaned_milestones = db.session.execute("SELECT count(*) FROM goal_milestones WHERE goal_id NOT IN (SELECT id FROM goals)").scalar() or 0

        is_clean = (orphaned_subtasks == 0) and (orphaned_milestones == 0)

        return {
            "status": "healthy" if is_clean else "anomalies_detected",
            "orphaned_subtasks_count": orphaned_subtasks,
            "orphaned_milestones_count": orphaned_milestones,
            "integrity_passed": is_clean
        }
