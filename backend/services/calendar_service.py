"""
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
