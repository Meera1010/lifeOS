"""
LifeOS Focus & Pomodoro Domain Service — Comprehensive Business Logic
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Optional
from sqlalchemy import func, or_, and_, desc, asc
from backend.models.base import db
from backend.models.focus import FocusSession, DistractionLog, PomodoroSetting, DailyFocusSummary
from backend.security.validators import sanitize_string
from backend.utilities.date_utils import parse_datetime_string, parse_date_string, get_month_range, get_week_range


class FocusService:
    """
    Comprehensive Focus & Deep Work Domain Service providing:
    - Pomodoro clock session timer lifecycle management
    - Interruption and distraction logging during deep work sessions
    - Focus rating (1 to 5 stars) and session productivity feedback
    - Daily & weekly deep work total time accumulation
    - Custom Pomodoro duration settings (work mins, short break, long break)
    - Flow-state continuity analytics and focus interruption cost metrics
    """

    @staticmethod
    def get_user_focus_sessions(user_id: int, days: int = 7) -> List[Dict]:
        """Retrieves user focus sessions for the past N days."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        sessions = FocusSession.query.filter(
            FocusSession.user_id == user_id,
            FocusSession.created_at >= cutoff
        ).order_by(desc(FocusSession.created_at)).all()

        return [s.to_dict() for s in sessions]

    @staticmethod
    def start_focus_session(user_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Starts a new Pomodoro or Deep Work session."""
        try:
            target_mins = max(1, int(data.get("target_minutes", 25)))
        except (ValueError, TypeError):
            target_mins = 25

        session_type = data.get("session_type", "pomodoro")
        task_id = data.get("task_id")

        session = FocusSession(
            user_id=user_id,
            task_id=task_id,
            session_type=session_type,
            duration_minutes=target_mins,
            actual_minutes=0,
            completed_at=datetime.utcnow(),
            is_completed=False,
            distraction_count=0
        )
        db.session.add(session)
        db.session.commit()
        return True, session.to_dict()

    @staticmethod
    def complete_focus_session(user_id: int, session_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Completes a focus session with actual duration and user rating."""
        session = FocusSession.query.filter_by(id=session_id, user_id=user_id).first()
        if not session:
            return False, {"error": "Focus session not found."}

        try:
            actual_mins = max(1, int(data.get("actual_minutes", session.duration_minutes)))
            rating = max(1, min(5, int(data.get("focus_rating", 5))))
        except (ValueError, TypeError):
            actual_mins = session.target_minutes
            rating = 5

        session.actual_minutes = actual_mins
        session.completed_at = datetime.utcnow()
        session.is_completed = True
        session.productivity_rating = rating
        session.notes = sanitize_string(data.get("notes", ""))

        db.session.commit()
        return True, session.to_dict()

    @staticmethod
    def log_distraction(user_id: int, session_id: int, description: str) -> Tuple[bool, Dict]:
        """Logs an interruption or distraction event during a focus session."""
        session = FocusSession.query.filter_by(id=session_id, user_id=user_id).first()
        if not session:
            return False, {"error": "Focus session not found."}

        desc_str = sanitize_string(description)
        if not desc_str:
            return False, {"error": "Distraction description is required."}

        distraction = DistractionLog(
            focus_session_id=session.id,
            description=desc_str,
            category=sanitize_string(description.get("category", "General") if isinstance(description, dict) else "General"),
            timestamp=datetime.utcnow()
        )
        db.session.add(distraction)

        session.distraction_count = (session.distraction_count or 0) + 1
        db.session.commit()
        return True, session.to_dict()

    @staticmethod
    def get_user_settings(user_id: int) -> Dict:
        """Retrieves or initializes user Pomodoro settings."""
        settings = PomodoroSetting.query.filter_by(user_id=user_id).first()
        if not settings:
            settings = PomodoroSetting(
                user_id=user_id,
                work_duration_minutes=25,
                short_break_minutes=5,
                long_break_minutes=15,
                long_break_interval=4,
                auto_start_breaks=False
            )
            db.session.add(settings)
            db.session.commit()

        return settings.to_dict()

    @staticmethod
    def update_user_settings(user_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Updates user Pomodoro timer configuration."""
        settings = PomodoroSetting.query.filter_by(user_id=user_id).first()
        if not settings:
            settings = PomodoroSetting(user_id=user_id)
            db.session.add(settings)

        try:
            settings.work_duration_minutes = max(1, int(data.get("work_duration_minutes", 25)))
            settings.short_break_minutes = max(1, int(data.get("short_break_minutes", 5)))
            settings.long_break_minutes = max(1, int(data.get("long_break_minutes", 15)))
            settings.long_break_interval = max(1, int(data.get("long_break_interval", 4)))
        except (ValueError, TypeError):
            pass

        settings.auto_start_breaks = bool(data.get("auto_start_breaks", False))
        db.session.commit()
        return True, settings.to_dict()
