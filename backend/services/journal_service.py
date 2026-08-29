"""
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
