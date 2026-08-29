"""
LifeOS Calendar Collision & Conflict Resolution Service
"""

from datetime import datetime, timedelta
from typing import List, Dict
from backend.services.calendar_service import CalendarService
from backend.utilities.date_utils import parse_datetime_string

class EventCollisionService:

    @staticmethod
    def detect_event_conflicts(user_id: int, start_dt_str: str, end_dt_str: str) -> Dict:
        """
        Detects schedule overlaps and collision conflicts for proposed calendar event.
        """
        start_dt = parse_datetime_string(start_dt_str)
        end_dt = parse_datetime_string(end_dt_str)

        events = CalendarService.get_events_for_range(user_id, start_dt, end_dt)
        conflicts = []

        for e in events:
            ev_start = parse_datetime_string(e["start_time"])
            ev_end = parse_datetime_string(e["end_time"])

            # Check overlap logic: (StartA < EndB) and (EndA > StartB)
            if start_dt < ev_end and end_dt > ev_start:
                conflicts.append(e)

        return {
            "has_conflict": len(conflicts) > 0,
            "conflict_count": len(conflicts),
            "conflicting_events": conflicts
        }

    @staticmethod
    def suggest_next_free_slot(user_id: int, duration_minutes: int = 60, preferred_date_str: str = None) -> Dict:
        """Finds next available un-conflicted calendar slot."""
        start_search = parse_datetime_string(preferred_date_str) if preferred_date_str else datetime.utcnow()
        end_search = start_search + timedelta(days=7)

        events = CalendarService.get_events_for_range(user_id, start_search, end_search)
        
        current_candidate = start_search
        slot_found = None

        while current_candidate < end_search:
            candidate_end = current_candidate + timedelta(minutes=duration_minutes)
            has_overlap = False

            for e in events:
                ev_start = parse_datetime_string(e["start_time"])
                ev_end = parse_datetime_string(e["end_time"])
                if current_candidate < ev_end and candidate_end > ev_start:
                    has_overlap = True
                    current_candidate = ev_end
                    break

            if not has_overlap:
                slot_found = {
                    "start_time": current_candidate.isoformat(),
                    "end_time": candidate_end.isoformat()
                }
                break

        return {
            "suggested_slot": slot_found
        }
