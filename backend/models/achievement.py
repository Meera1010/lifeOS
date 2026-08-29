"""
LifeOS Gamification & Achievement Models
"""

from datetime import datetime
from backend.models.base import db, TimestampMixin, SerializerMixin

class Achievement(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True) # e.g. FIRST_TASK
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), default="General", nullable=False) # Tasks, Habits, Goals, Focus, Finance, Learning, General
    icon = db.Column(db.String(50), default="award", nullable=False)
    color = db.Column(db.String(20), default="#f59e0b", nullable=False)
    badge_tier = db.Column(db.String(20), default="bronze", nullable=False) # bronze, silver, gold, platinum, diamond
    points = db.Column(db.Integer, default=50, nullable=False)
    threshold = db.Column(db.Integer, default=1, nullable=False)
    is_hidden = db.Column(db.Boolean, default=False, nullable=False)

    user_achievements = db.relationship("UserAchievement", backref="achievement", cascade="all, delete-orphan")


class UserAchievement(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "user_achievements"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    achievement_id = db.Column(db.Integer, db.ForeignKey("achievements.id"), nullable=False, index=True)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    progress = db.Column(db.Integer, default=1, nullable=False)
    is_notified = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self, exclude=None, include_relationships=True):
        data = super().to_dict(exclude=exclude)
        if include_relationships and self.achievement:
            data["achievement"] = self.achievement.to_dict()
        return data


class AchievementProgress(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "achievement_progresses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    achievement_id = db.Column(db.Integer, db.ForeignKey("achievements.id"), nullable=False)
    current_value = db.Column(db.Integer, default=0, nullable=False)
    target_value = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, default=0.0, nullable=False)
