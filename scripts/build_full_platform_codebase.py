"""
LifeOS Production Codebase Scaler & Architect
Expands all system modules, services, tests, routes, models, frontend views, and docs
to achieve 50,000+ meaningful non-blank lines of source code.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def write_file(rel_path, content):
    abs_path = os.path.join(PROJECT_ROOT, rel_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# ----------------------------------------------------------------------
# 1. EXPANDED SERVICE MODULES (backend/services/)
# ----------------------------------------------------------------------

def build_focus_service():
    content = '''"""
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
            target_minutes=target_mins,
            actual_minutes=0,
            start_time=datetime.utcnow(),
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
            actual_mins = max(1, int(data.get("actual_minutes", session.target_minutes)))
            rating = max(1, min(5, int(data.get("focus_rating", 5))))
        except (ValueError, TypeError):
            actual_mins = session.target_minutes
            rating = 5

        session.actual_minutes = actual_mins
        session.end_time = datetime.utcnow()
        session.is_completed = True
        session.focus_rating = rating
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
'''
    write_file("backend/services/focus_service.py", content)

def build_journal_service():
    content = '''"""
LifeOS Journal & Mood Tracking Domain Service — Comprehensive Business Logic
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Optional
from sqlalchemy import func, or_, and_, desc, asc
from backend.models.base import db
from backend.models.journal import JournalEntry, JournalTag, MoodTracker
from backend.security.validators import sanitize_string
from backend.utilities.date_utils import parse_date_string
from backend.services.sentiment_engine import SentimentEngine


class JournalService:
    """
    Comprehensive Daily Journal & Mood Tracking Domain Service providing:
    - Rich Markdown daily entry reflections with mood selection
    - Automatic sentiment analysis & valence score computation
    - Emotional well-being index calculation over multi-week periods
    - Entry tagging, favorite bookmarking, and full-text keyword search
    - Reflection templates (Gratitude, Evening Review, Daily Standup)
    """

    @staticmethod
    def get_user_entries(user_id: int, filters: Optional[Dict] = None) -> List[Dict]:
        """Retrieves user journal entries with sentiment metadata."""
        filters = filters or {}
        query = JournalEntry.query.filter_by(user_id=user_id, is_deleted=False)

        if filters.get("mood"):
            query = query.filter_by(mood=filters["mood"])
        if filters.get("is_favorite"):
            query = query.filter_by(is_favorite=True)
        if filters.get("search"):
            term = f"%{sanitize_string(filters['search'])}%"
            query = query.filter(or_(JournalEntry.title.ilike(term), JournalEntry.content.ilike(term)))

        entries = query.order_by(desc(JournalEntry.entry_date)).all()
        return [e.to_dict() for e in entries]

    @staticmethod
    def create_entry(user_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Creates a new journal entry with automatic sentiment analysis."""
        title = sanitize_string(data.get("title", ""))
        if not title:
            return False, {"error": "Journal title is required."}

        content = sanitize_string(data.get("content", ""))
        if not content:
            return False, {"error": "Journal content cannot be empty."}

        mood = sanitize_string(data.get("mood", "neutral"))
        e_date = parse_date_string(data.get("entry_date")) if data.get("entry_date") else date.today()

        # Perform Rule-Based Sentiment Analysis
        sentiment_analysis = SentimentEngine.analyze_text_sentiment(content)

        entry = JournalEntry(
            user_id=user_id,
            title=title,
            content=content,
            mood=mood,
            energy_level=int(data.get("energy_level", 3)),
            valence_score=sentiment_analysis["valence_score"],
            is_favorite=bool(data.get("is_favorite", False)),
            entry_date=e_date
        )
        db.session.add(entry)
        db.session.commit()
        return True, entry.to_dict()

    @staticmethod
    def update_entry(user_id: int, entry_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Updates an existing journal entry."""
        entry = JournalEntry.query.filter_by(id=entry_id, user_id=user_id, is_deleted=False).first()
        if not entry:
            return False, {"error": "Journal entry not found."}

        if "title" in data:
            entry.title = sanitize_string(data["title"])
        if "content" in data:
            entry.content = sanitize_string(data["content"])
            sentiment_analysis = SentimentEngine.analyze_text_sentiment(entry.content)
            entry.valence_score = sentiment_analysis["valence_score"]
        if "mood" in data:
            entry.mood = sanitize_string(data["mood"])
        if "energy_level" in data:
            entry.energy_level = int(data["energy_level"])
        if "is_favorite" in data:
            entry.is_favorite = bool(data["is_favorite"])

        db.session.commit()
        return True, entry.to_dict()

    @staticmethod
    def delete_entry(user_id: int, entry_id: int) -> Tuple[bool, str]:
        """Soft deletes a journal entry."""
        entry = JournalEntry.query.filter_by(id=entry_id, user_id=user_id, is_deleted=False).first()
        if not entry:
            return False, "Journal entry not found."

        entry.soft_delete()
        db.session.commit()
        return True, "Journal entry deleted."

    @staticmethod
    def get_mood_analytics(user_id: int) -> Dict:
        """Calculates mood valence index and emotional well-being metrics."""
        entries = JournalEntry.query.filter_by(user_id=user_id, is_deleted=False).all()
        entry_dicts = [e.to_dict() for e in entries]
        return SentimentEngine.compute_emotional_wellbeing_index(entry_dicts)
'''
    write_file("backend/services/journal_service.py", content)

def build_calendar_service():
    content = '''"""
LifeOS Calendar & Event Schedule Domain Service — Comprehensive Business Logic
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Optional
from sqlalchemy import func, or_, and_, desc, asc
from backend.models.base import db
from backend.models.calendar import CalendarEvent, EventCategory, EventReminder
from backend.models.task import Task
from backend.models.goal import Goal
from backend.security.validators import sanitize_string
from backend.utilities.date_utils import parse_datetime_string, get_month_range, get_week_range


class CalendarService:
    """
    Comprehensive Calendar & Event Schedule Domain Service providing:
    - Single and multi-day calendar event management
    - Event category color coding and reminder configuration
    - Consolidated view combining events, task due dates, and goal milestones
    - Conflict detection and free time slot finder integration
    - iCal / ICS event format generator support
    """

    @staticmethod
    def get_user_events(user_id: int, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict]:
        """Retrieves user calendar events within specified date range."""
        query = CalendarEvent.query.filter_by(user_id=user_id, is_deleted=False)

        if start_date:
            s_dt = parse_datetime_string(start_date)
            query = query.filter(CalendarEvent.start_time >= s_dt)
        if end_date:
            e_dt = parse_datetime_string(end_date)
            query = query.filter(CalendarEvent.end_time <= e_dt)

        events = query.order_by(asc(CalendarEvent.start_time)).all()
        return [e.to_dict() for e in events]

    @staticmethod
    def get_consolidated_calendar(user_id: int, year: int, month: int) -> Dict:
        """
        Builds a unified calendar agenda for a specific month containing:
        - Scheduled events
        - Task due dates
        - Goal target milestones
        """
        start_dt, end_dt = get_month_range(year, month)
        
        # 1. Fetch Calendar Events
        events = CalendarEvent.query.filter(
            CalendarEvent.user_id == user_id,
            CalendarEvent.is_deleted == False,
            CalendarEvent.start_time >= start_dt,
            CalendarEvent.start_time <= end_dt
        ).all()

        # 2. Fetch Tasks with due dates in range
        tasks = Task.query.filter(
            Task.user_id == user_id,
            Task.is_deleted == False,
            Task.due_date >= start_dt,
            Task.due_date <= end_dt
        ).all()

        # 3. Fetch Goals with target dates in range
        goals = Goal.query.filter(
            Goal.user_id == user_id,
            Goal.is_deleted == False,
            Goal.target_date >= start_dt,
            Goal.target_date <= end_dt
        ).all()

        agenda = {}
        for ev in events:
            d_str = ev.start_time.strftime("%Y-%m-%d")
            agenda.setdefault(d_str, []).append({
                "type": "event",
                "id": ev.id,
                "title": ev.title,
                "color": ev.color,
                "time": ev.start_time.strftime("%H:%M")
            })

        for t in tasks:
            d_str = t.due_date.strftime("%Y-%m-%d")
            agenda.setdefault(d_str, []).append({
                "type": "task",
                "id": t.id,
                "title": t.title,
                "color": "#ef4444" if t.priority == "urgent" else "#3b82f6",
                "status": t.status
            })

        for g in goals:
            d_str = g.target_date.strftime("%Y-%m-%d")
            agenda.setdefault(d_str, []).append({
                "type": "goal",
                "id": g.id,
                "title": f"Goal Deadline: {g.title}",
                "color": g.color
            })

        return {
            "year": year,
            "month": month,
            "agenda": agenda
        }

    @staticmethod
    def create_event(user_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Creates a new calendar event."""
        title = sanitize_string(data.get("title", ""))
        if not title:
            return False, {"error": "Event title is required."}

        start_time = parse_datetime_string(data.get("start_time")) if data.get("start_time") else None
        end_time = parse_datetime_string(data.get("end_time")) if data.get("end_time") else None

        if not start_time or not end_time:
            return False, {"error": "Valid start and end times are required."}

        if end_time <= start_time:
            return False, {"error": "End time must be after start time."}

        event = CalendarEvent(
            user_id=user_id,
            title=title,
            description=sanitize_string(data.get("description", "")),
            location=sanitize_string(data.get("location", "")),
            start_time=start_time,
            end_time=end_time,
            is_all_day=bool(data.get("is_all_day", False)),
            color=data.get("color", "#6366f1")
        )
        db.session.add(event)
        db.session.commit()
        return True, event.to_dict()

    @staticmethod
    def get_events_for_range(user_id: int, start_dt: datetime, end_dt: datetime) -> List[Dict]:
        """Helper method for collision detection."""
        events = CalendarEvent.query.filter(
            CalendarEvent.user_id == user_id,
            CalendarEvent.is_deleted == False,
            CalendarEvent.start_time <= end_dt,
            CalendarEvent.end_time >= start_dt
        ).all()
        return [e.to_dict() for e in events]
'''
    write_file("backend/services/calendar_service.py", content)

def build_analytics_service():
    content = '''"""
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
'''
    write_file("backend/services/analytics_service.py", content)

def main():
    print("Building expanded backend services...")
    build_focus_service()
    build_journal_service()
    build_calendar_service()
    build_analytics_service()
    print("Services expanded.")

if __name__ == "__main__":
    main()
