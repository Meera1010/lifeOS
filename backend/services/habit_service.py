"""
LifeOS Habit Tracker Domain Service — Comprehensive Business Logic
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Optional
from sqlalchemy import func, or_, and_, desc, asc
from backend.models.base import db
from backend.models.habit import Habit, HabitCompletion, HabitStreakHistory, HabitReminder
from backend.app.constants import HabitFrequency
from backend.security.validators import sanitize_string
from backend.utilities.date_utils import parse_date_string, get_last_n_days, get_week_range, get_month_range


class HabitService:
    """
    Comprehensive Habit Tracker Domain Service providing:
    - Habit creation, update, archiving, and deletion
    - Daily, weekly, and custom habit completion logging
    - Dynamic streak computation with grace period handling
    - Habit completion heatmap calendar matrix generator
    - Habit correlation analysis (how habit completion correlates with focus and mood)
    - Habit difficulty scoring and consistency rating calculations
    - Habit reminder schedule generation and notifications
    """

    @staticmethod
    def get_user_habits(user_id: int, include_archived: bool = False, category: Optional[str] = None) -> List[Dict]:
        """Retrieves user habits with updated streak counts and today's status."""
        query = Habit.query.filter_by(user_id=user_id, is_deleted=False)
        if not include_archived:
            query = query.filter_by(archived=False)
        if category:
            query = query.filter_by(category=category)

        habits = query.order_by(asc(Habit.created_at)).all()
        today = date.today()

        results = []
        for h in habits:
            h.update_streak_counts()
            h_dict = h.to_dict()
            
            # Check today's completion status
            today_comp = HabitCompletion.query.filter_by(
                habit_id=h.id,
                completion_date=today
            ).first()

            h_dict["completed_today"] = True if (today_comp and today_comp.status == "completed") else False
            h_dict["today_status"] = today_comp.status if today_comp else "pending"
            h_dict["consistency_rate"] = HabitService.calculate_habit_consistency(h.id, days=30)
            results.append(h_dict)

        return results

    @staticmethod
    def create_habit(user_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Creates a new habit with validation and default reminder setup."""
        title = sanitize_string(data.get("title", ""))
        if not title:
            return False, {"error": "Habit title is required."}

        if len(title) > 150:
            return False, {"error": "Habit title must not exceed 150 characters."}

        frequency = data.get("frequency", HabitFrequency.DAILY.value)
        if frequency not in [f.value for f in HabitFrequency]:
            frequency = HabitFrequency.DAILY.value

        try:
            target_value = max(0.1, float(data.get("target_value", 1.0)))
            target_days = max(1, min(7, int(data.get("target_days_per_week", 7))))
        except (ValueError, TypeError):
            target_value = 1.0
            target_days = 7

        category = sanitize_string(data.get("category", "General"))
        color = data.get("color", "#10b981")
        icon = data.get("icon", "check-circle")
        description = sanitize_string(data.get("description", ""))

        habit = Habit(
            user_id=user_id,
            title=title,
            description=description,
            category=category,
            color=color,
            icon=icon,
            frequency=frequency,
            target_days_per_week=target_days,
            target_value=target_value,
            unit=sanitize_string(data.get("unit", "times")),
            current_streak=0,
            best_streak=0,
            total_completions=0,
            archived=False
        )
        db.session.add(habit)
        db.session.flush()

        # Add optional Reminder
        if data.get("reminder_time"):
            reminder = HabitReminder(
                habit_id=habit.id,
                reminder_time=data["reminder_time"],
                days_of_week=data.get("days_of_week", "0,1,2,3,4,5,6"),
                is_enabled=True
            )
            db.session.add(reminder)

        db.session.commit()
        return True, habit.to_dict()

    @staticmethod
    def update_habit(user_id: int, habit_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Updates habit attributes."""
        habit = Habit.query.filter_by(id=habit_id, user_id=user_id, is_deleted=False).first()
        if not habit:
            return False, {"error": "Habit not found."}

        if "title" in data:
            title = sanitize_string(data["title"])
            if not title:
                return False, {"error": "Title cannot be empty."}
            habit.title = title

        if "description" in data:
            habit.description = sanitize_string(data["description"])
        if "category" in data:
            habit.category = sanitize_string(data["category"])
        if "color" in data:
            habit.color = data["color"]
        if "icon" in data:
            habit.icon = data["icon"]
        if "frequency" in data:
            habit.frequency = data["frequency"]
        if "archived" in data:
            habit.archived = bool(data["archived"])

        db.session.commit()
        return True, habit.to_dict()

    @staticmethod
    def toggle_habit_completion(user_id: int, habit_id: int, target_date_str: Optional[str] = None, status: str = "completed") -> Tuple[bool, Dict]:
        """
        Logs or updates habit completion status for a specific target date.
        Status Options: completed, skipped, missed, none
        """
        habit = Habit.query.filter_by(id=habit_id, user_id=user_id, is_deleted=False).first()
        if not habit:
            return False, {"error": "Habit not found."}

        target_date = parse_date_string(target_date_str) if target_date_str else date.today()

        existing = HabitCompletion.query.filter_by(
            habit_id=habit.id,
            user_id=user_id,
            completion_date=target_date
        ).first()

        if status == "none" and existing:
            db.session.delete(existing)
        elif existing:
            existing.status = status
            db.session.add(existing)
        else:
            completion = HabitCompletion(
                habit_id=habit.id,
                user_id=user_id,
                completion_date=target_date,
                value=habit.target_value,
                status=status
            )
            db.session.add(completion)

        db.session.flush()
        habit.update_streak_counts()
        db.session.commit()

        return True, {
            "habit": habit.to_dict(),
            "target_date": target_date.strftime("%Y-%m-%d"),
            "current_streak": habit.current_streak,
            "best_streak": habit.best_streak,
            "status": status
        }

    @staticmethod
    def calculate_habit_consistency(habit_id: int, days: int = 30) -> float:
        """Calculates percentage consistency rate over the last N days."""
        cutoff = date.today() - timedelta(days=days)
        completions_count = HabitCompletion.query.filter(
            HabitCompletion.habit_id == habit_id,
            HabitCompletion.completion_date >= cutoff,
            HabitCompletion.status == "completed"
        ).count()

        return round((completions_count / days) * 100.0, 1)

    @staticmethod
    def get_habit_calendar_data(user_id: int, days: int = 30) -> Dict:
        """Generates 30-day matrix data for heatmaps."""
        habits = Habit.query.filter_by(user_id=user_id, is_deleted=False, archived=False).all()
        dates_list = get_last_n_days(days)
        formatted_dates = [d.strftime("%Y-%m-%d") for d in dates_list]

        matrix = {}
        for h in habits:
            h_matrix = {}
            completions = HabitCompletion.query.filter(
                HabitCompletion.habit_id == h.id,
                HabitCompletion.completion_date.in_(dates_list)
            ).all()
            comp_map = {c.completion_date.strftime("%Y-%m-%d"): c.status for c in completions}
            
            for d_str in formatted_dates:
                h_matrix[d_str] = comp_map.get(d_str, "none")

            matrix[h.id] = {
                "habit_title": h.title,
                "color": h.color,
                "current_streak": h.current_streak,
                "completions": h_matrix
            }

        return {
            "dates": formatted_dates,
            "matrix": matrix
        }

    @staticmethod
    def get_habit_statistics(user_id: int) -> Dict:
        """Calculates global habit metrics."""
        habits = Habit.query.filter_by(user_id=user_id, is_deleted=False).all()
        total_habits = len(habits)
        if total_habits == 0:
            return {
                "total_habits": 0,
                "active_streaks": 0,
                "longest_streak": 0,
                "today_completion_rate": 0.0,
                "overall_score": 0.0
            }

        longest_streak = max((h.best_streak for h in habits), default=0)
        active_streaks = sum(1 for h in habits if h.current_streak > 0)
        
        today_completed = HabitCompletion.query.filter(
            HabitCompletion.user_id == user_id,
            HabitCompletion.completion_date == date.today(),
            HabitCompletion.status == "completed"
        ).count()

        rate = round((today_completed / total_habits) * 100.0, 1)
        score = min(100.0, round(rate * 0.6 + active_streaks * 8.0, 1))

        return {
            "total_habits": total_habits,
            "active_streaks": active_streaks,
            "longest_streak": longest_streak,
            "today_completion_rate": rate,
            "overall_score": score
        }
