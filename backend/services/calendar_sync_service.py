"""
LifeOS iCal & ICS Calendar Import/Export Sync Service
"""

from datetime import datetime
from typing import Dict, Any, List
from backend.models.calendar import CalendarEvent


class CalendarSyncService:
    """
    Parses and generates iCalendar (ICS) event feeds for external calendar integration.
    """

    @staticmethod
    def generate_ics_feed(user_id: int) -> str:
        """Generates iCalendar (.ics) formatted string feed."""
        events = CalendarEvent.query.filter_by(user_id=user_id, is_deleted=False).all()
        
        ics = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//LifeOS//Personal Life Platform//EN\n"
        for ev in events:
            s_str = ev.start_time.strftime("%Y%m%dT%H%M%SZ")
            e_str = ev.end_time.strftime("%Y%m%dT%H%M%SZ")
            ics += "BEGIN:VEVENT\n"
            ics += f"UID:lifeos_ev_{ev.id}@lifeos.local\n"
            ics += f"SUMMARY:{ev.title}\n"
            ics += f"DTSTART:{s_str}\n"
            ics += f"DTEND:{e_str}\n"
            if ev.description:
                ics += f"DESCRIPTION:{ev.description}\n"
            ics += "END:VEVENT\n"

        ics += "END:VCALENDAR"
        return ics
