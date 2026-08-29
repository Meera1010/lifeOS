"""
LifeOS Full Scale Core Platform Builder — Builds comprehensive services and unit tests.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def write_file(rel_path, content):
    abs_path = os.path.join(PROJECT_ROOT, rel_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_services():
    # 1. calendar_sync_service.py
    write_file("backend/services/calendar_sync_service.py", '''"""
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
        
        ics = "BEGIN:VCALENDAR\\nVERSION:2.0\\nPRODID:-//LifeOS//Personal Life Platform//EN\\n"
        for ev in events:
            s_str = ev.start_time.strftime("%Y%m%dT%H%M%SZ")
            e_str = ev.end_time.strftime("%Y%m%dT%H%M%SZ")
            ics += "BEGIN:VEVENT\\n"
            ics += f"UID:lifeos_ev_{ev.id}@lifeos.local\\n"
            ics += f"SUMMARY:{ev.title}\\n"
            ics += f"DTSTART:{s_str}\\n"
            ics += f"DTEND:{e_str}\\n"
            if ev.description:
                ics += f"DESCRIPTION:{ev.description}\\n"
            ics += "END:VEVENT\\n"

        ics += "END:VCALENDAR"
        return ics
''')

    # 2. notification_rule_engine.py
    write_file("backend/services/notification_rule_engine.py", '''"""
LifeOS Automated Notification Dispatch Rule Engine
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Any
from backend.models.base import db
from backend.models.task import Task
from backend.services.notification_service import NotificationService


class NotificationRuleEngine:
    """
    Scans system events and dispatches automated reminder notifications.
    """

    @staticmethod
    def check_upcoming_task_deadlines(user_id: int) -> int:
        """Dispatches notifications for tasks due within the next 24 hours."""
        now = datetime.utcnow()
        cutoff = now + timedelta(hours=24)

        tasks = Task.query.filter(
            Task.user_id == user_id,
            Task.is_deleted == False,
            Task.status != "completed",
            Task.due_date >= now,
            Task.due_date <= cutoff
        ).all()

        dispatched = 0
        for t in tasks:
            NotificationService.create_notification(
                user_id=user_id,
                title=f"Task Due Soon: {t.title}",
                message=f"Task '{t.title}' is due within 24 hours.",
                notification_type="task_due",
                severity="warning",
                entity_type="task",
                entity_id=t.id
            )
            dispatched += 1

        return dispatched
''')

def main():
    print("Building calendar sync and notification rule engine...")
    generate_services()
    print("Generation complete.")

if __name__ == "__main__":
    main()
