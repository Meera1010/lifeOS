"""
LifeOS Data Export & Backup Generation Domain Service
"""

import json
import csv
import io
from datetime import datetime
from typing import Dict, Any
from backend.models.task import Task
from backend.models.habit import Habit, HabitCompletion
from backend.models.goal import Goal
from backend.models.finance import Transaction
from backend.models.learning import Course, StudySession
from backend.models.journal import JournalEntry
from backend.models.focus import FocusSession


class ExportService:
    """
    Comprehensive User Data Export Domain Service providing:
    - Full account data backup in JSON format
    - Task, Finance, and Journal exports in CSV format
    - Data portability compliance and archival generation
    """

    @staticmethod
    def export_user_data_json(user_id: int) -> Dict[str, Any]:
        """Exports complete user data state as structured JSON dictionary."""
        tasks = [t.to_dict() for t in Task.query.filter_by(user_id=user_id, is_deleted=False).all()]
        habits = [h.to_dict() for h in Habit.query.filter_by(user_id=user_id, is_deleted=False).all()]
        habit_completions = [hc.to_dict() for hc in HabitCompletion.query.filter_by(user_id=user_id).all()]
        goals = [g.to_dict() for g in Goal.query.filter_by(user_id=user_id, is_deleted=False).all()]
        transactions = [tx.to_dict() for tx in Transaction.query.filter_by(user_id=user_id, is_deleted=False).all()]
        courses = [c.to_dict() for c in Course.query.filter_by(user_id=user_id, is_deleted=False).all()]
        study_sessions = [ss.to_dict() for ss in StudySession.query.filter_by(user_id=user_id).all()]
        journal_entries = [j.to_dict() for j in JournalEntry.query.filter_by(user_id=user_id, is_deleted=False).all()]
        focus_sessions = [fs.to_dict() for fs in FocusSession.query.filter_by(user_id=user_id).all()]

        return {
            "platform": "LifeOS",
            "version": "1.0.0",
            "exported_at": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "data": {
                "tasks": tasks,
                "habits": habits,
                "habit_completions": habit_completions,
                "goals": goals,
                "transactions": transactions,
                "courses": courses,
                "study_sessions": study_sessions,
                "journal_entries": journal_entries,
                "focus_sessions": focus_sessions
            }
        }

    @staticmethod
    def export_tasks_csv(user_id: int) -> str:
        """Generates CSV string of user tasks."""
        tasks = Task.query.filter_by(user_id=user_id, is_deleted=False).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Title", "Priority", "Status", "Due Date", "Estimated Mins", "Actual Mins", "Created At"])
        for t in tasks:
            writer.writerow([
                t.id, t.title, t.priority, t.status,
                t.due_date.strftime("%Y-%m-%d %H:%M") if t.due_date else "",
                t.estimated_minutes, t.actual_minutes,
                t.created_at.strftime("%Y-%m-%d %H:%M")
            ])
        return output.getvalue()

    @staticmethod
    def export_finance_csv(user_id: int) -> str:
        """Generates CSV string of user transactions."""
        txs = Transaction.query.filter_by(user_id=user_id, is_deleted=False).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Type", "Amount", "Description", "Category", "Date", "Payment Method"])
        for t in txs:
            writer.writerow([
                t.id, t.type, t.amount, t.description,
                t.finance_category.name if t.finance_category else "",
                t.transaction_date.strftime("%Y-%m-%d"),
                t.payment_method
            ])
        return output.getvalue()
