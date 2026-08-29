"""
LifeOS Journal & Reflection Models
"""

from datetime import datetime, date
from backend.models.base import db, TimestampMixin, SoftDeleteMixin, SerializerMixin
from backend.app.constants import MoodType

entry_tags_table = db.Table(
    "journal_entry_tags",
    db.Column("entry_id", db.Integer, db.ForeignKey("journal_entries.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("journal_tags.id"), primary_key=True)
)

class JournalTag(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "journal_tags"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), default="#ec4899", nullable=False)


class JournalEntry(db.Model, TimestampMixin, SoftDeleteMixin, SerializerMixin):
    __tablename__ = "journal_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    entry_date = db.Column(db.Date, default=date.today, nullable=False, index=True)
    mood = db.Column(db.String(30), default=MoodType.GOOD.value, nullable=False, index=True)
    energy_level = db.Column(db.Integer, default=7, nullable=False) # 1 to 10
    location = db.Column(db.String(100), nullable=True)
    weather = db.Column(db.String(50), nullable=True)
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    is_favorite = db.Column(db.Boolean, default=False, nullable=False)
    valence_score = db.Column(db.Float, default=0.0, nullable=False)

    tags = db.relationship("JournalTag", secondary=entry_tags_table, backref=db.backref("entries", lazy="dynamic"))

    def to_dict(self, exclude=None, include_relationships=True):
        data = super().to_dict(exclude=exclude)
        if isinstance(self.entry_date, (date, datetime)):
            data["entry_date"] = self.entry_date.strftime("%Y-%m-%d")
        if include_relationships:
            data["tags"] = [t.to_dict() for t in self.tags]
        return data


class MoodTracker(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "journal_mood_trackers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    log_date = db.Column(db.Date, default=date.today, nullable=False, index=True)
    mood = db.Column(db.String(30), nullable=False)
    valence_score = db.Column(db.Float, default=0.5, nullable=False) # -1.0 to +1.0
    notes = db.Column(db.String(255), nullable=True)

    def to_dict(self, exclude=None):
        data = super().to_dict(exclude=exclude)
        if isinstance(self.log_date, (date, datetime)):
            data["log_date"] = self.log_date.strftime("%Y-%m-%d")
        return data
