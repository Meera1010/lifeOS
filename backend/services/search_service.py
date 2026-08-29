"""
LifeOS Global Search Engine
"""

from sqlalchemy import or_
from backend.models.task import Task
from backend.models.habit import Habit
from backend.models.goal import Goal
from backend.models.calendar import CalendarEvent
from backend.models.finance import Transaction
from backend.models.learning import Course
from backend.models.journal import JournalEntry

class SearchService:

    @staticmethod
    def global_search(user_id: int, query_term: str) -> dict:
        """
        Executes unified full-text global search across:
        - Tasks
        - Habits
        - Goals
        - Calendar Events
        - Financial Transactions
        - Learning Courses
        - Journal Entries
        """
        if not query_term or len(query_term.strip()) < 2:
            return {
                "query": query_term,
                "total_results": 0,
                "results": []
            }

        term = f"%{query_term.strip()}%"
        results = []

        # 1. Tasks Search
        tasks = Task.query.filter(
            Task.user_id == user_id,
            Task.is_deleted == False,
            or_(Task.title.ilike(term), Task.description.ilike(term))
        ).limit(10).all()

        for t in tasks:
            results.append({
                "type": "task",
                "id": t.id,
                "title": t.title,
                "subtitle": f"Priority: {t.priority.upper()} | Status: {t.status}",
                "snippet": t.description or "",
                "url": f"/tasks?id={t.id}",
                "icon": "check-square"
            })

        # 2. Habits Search
        habits = Habit.query.filter(
            Habit.user_id == user_id,
            Habit.is_deleted == False,
            or_(Habit.title.ilike(term), Habit.description.ilike(term))
        ).limit(10).all()

        for h in habits:
            results.append({
                "type": "habit",
                "id": h.id,
                "title": h.title,
                "subtitle": f"Streak: {h.current_streak} days | Frequency: {h.frequency}",
                "snippet": h.description or "",
                "url": f"/habits?id={h.id}",
                "icon": "repeat"
            })

        # 3. Goals Search
        goals = Goal.query.filter(
            Goal.user_id == user_id,
            Goal.is_deleted == False,
            or_(Goal.title.ilike(term), Goal.description.ilike(term))
        ).limit(10).all()

        for g in goals:
            results.append({
                "type": "goal",
                "id": g.id,
                "title": g.title,
                "subtitle": f"Category: {g.category} | Progress: {g.progress_percentage}%",
                "snippet": g.description or "",
                "url": f"/goals?id={g.id}",
                "icon": "target"
            })

        # 4. Calendar Events Search
        events = CalendarEvent.query.filter(
            CalendarEvent.user_id == user_id,
            CalendarEvent.is_deleted == False,
            or_(CalendarEvent.title.ilike(term), CalendarEvent.description.ilike(term))
        ).limit(10).all()

        for e in events:
            results.append({
                "type": "event",
                "id": e.id,
                "title": e.title,
                "subtitle": f"Start: {e.start_time.strftime('%Y-%m-%d %H:%M')}",
                "snippet": e.description or "",
                "url": f"/calendar?id={e.id}",
                "icon": "calendar"
            })

        # 5. Financial Transactions Search
        txs = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.is_deleted == False,
            or_(Transaction.description.ilike(term), Transaction.notes.ilike(term))
        ).limit(10).all()

        for tx in txs:
            results.append({
                "type": "transaction",
                "id": tx.id,
                "title": tx.description,
                "subtitle": f"Type: {tx.type.upper()} | Amount: ${tx.amount}",
                "snippet": tx.notes or "",
                "url": f"/finance?id={tx.id}",
                "icon": "dollar-sign"
            })

        # 6. Courses Search
        courses = Course.query.filter(
            Course.user_id == user_id,
            Course.is_deleted == False,
            or_(Course.title.ilike(term), Course.notes.ilike(term))
        ).limit(10).all()

        for c in courses:
            results.append({
                "type": "course",
                "id": c.id,
                "title": c.title,
                "subtitle": f"Provider: {c.provider} | Progress: {c.progress_percentage}%",
                "snippet": c.notes or "",
                "url": f"/learning?id={c.id}",
                "icon": "book-open"
            })

        # 7. Journal Entries Search
        journals = JournalEntry.query.filter(
            JournalEntry.user_id == user_id,
            JournalEntry.is_deleted == False,
            or_(JournalEntry.title.ilike(term), JournalEntry.content.ilike(term))
        ).limit(10).all()

        for j in journals:
            results.append({
                "type": "journal",
                "id": j.id,
                "title": j.title,
                "subtitle": f"Date: {j.entry_date} | Mood: {j.mood}",
                "snippet": j.content[:150] + "..." if len(j.content) > 150 else j.content,
                "url": f"/journal?id={j.id}",
                "icon": "book"
            })

        return {
            "query": query_term,
            "total_results": len(results),
            "results": results
        }
