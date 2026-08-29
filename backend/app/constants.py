"""
LifeOS System Constants, Enums, Definitions & Configuration Defaults
"""

import enum

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class PriorityLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class HabitFrequency(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"

class GoalCategory(str, enum.Enum):
    PERSONAL = "personal"
    CAREER = "career"
    FINANCIAL = "financial"
    LEARNING = "learning"
    HEALTH = "health"
    RELATIONSHIPS = "relationships"

class GoalTimeframe(str, enum.Enum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"

class GoalStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class FinanceCategoryType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class FocusSessionType(str, enum.Enum):
    POMODORO = "pomodoro"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"
    DEEP_WORK = "deep_work"

class MoodType(str, enum.Enum):
    GREAT = "great"
    GOOD = "good"
    NEUTRAL = "neutral"
    LOW = "low"
    BAD = "bad"

class NotificationType(str, enum.Enum):
    TASK_REMINDER = "task_reminder"
    HABIT_REMINDER = "habit_reminder"
    GOAL_DEADLINE = "goal_deadline"
    BUDGET_ALERT = "budget_alert"
    STUDY_REMINDER = "study_reminder"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    SYSTEM_ALERT = "system_alert"

class NotificationSeverity(str, enum.Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"

# Default System Categories
DEFAULT_TASK_CATEGORIES = [
    {"name": "Work", "color": "#4f46e5", "icon": "briefcase"},
    {"name": "Personal", "color": "#06b6d4", "icon": "user"},
    {"name": "Health", "color": "#10b981", "icon": "activity"},
    {"name": "Finance", "color": "#f59e0b", "icon": "dollar-sign"},
    {"name": "Education", "color": "#8b5cf6", "icon": "book-open"},
    {"name": "Home", "color": "#ec4899", "icon": "home"}
]

DEFAULT_FINANCE_CATEGORIES = [
    {"name": "Salary", "type": "income", "color": "#10b981", "icon": "dollar-sign"},
    {"name": "Freelance", "type": "income", "color": "#06b6d4", "icon": "briefcase"},
    {"name": "Investments", "type": "income", "color": "#8b5cf6", "icon": "trending-up"},
    {"name": "Housing & Rent", "type": "expense", "color": "#ef4444", "icon": "home"},
    {"name": "Food & Dining", "type": "expense", "color": "#f59e0b", "icon": "shopping-bag"},
    {"name": "Transportation", "type": "expense", "color": "#3b82f6", "icon": "truck"},
    {"name": "Utilities & Bills", "type": "expense", "color": "#64748b", "icon": "zap"},
    {"name": "Entertainment", "type": "expense", "color": "#ec4899", "icon": "film"},
    {"name": "Health & Fitness", "type": "expense", "color": "#14b8a6", "icon": "heart"},
    {"name": "Education & Books", "type": "expense", "color": "#a855f7", "icon": "book"}
]

# Life Score Weightings (Total = 100%)
LIFE_SCORE_WEIGHTS = {
    "productivity": 0.20,
    "habits": 0.20,
    "goals": 0.20,
    "learning": 0.15,
    "finance": 0.15,
    "focus": 0.10
}
