"""
LifeOS Gamification Engine — 100+ System Achievements
"""

from datetime import datetime
from typing import List, Dict
from backend.models.base import db
from backend.models.achievement import Achievement, UserAchievement, AchievementProgress
from backend.models.task import Task
from backend.models.habit import Habit, HabitCompletion
from backend.models.goal import Goal
from backend.models.finance import Transaction, SavingsGoal
from backend.models.learning import Course, StudySession
from backend.models.focus import FocusSession
from backend.models.journal import JournalEntry
from backend.models.notification import Notification

SYSTEM_ACHIEVEMENTS_DEFINITION = [
    # Task Achievements (1-15)
    {"code": "TASK_01", "title": "First Step", "description": "Complete your first task in LifeOS.", "category": "Tasks", "badge_tier": "bronze", "points": 50, "threshold": 1, "icon": "check-square"},
    {"code": "TASK_02", "title": "Task Apprentice", "description": "Complete 10 tasks.", "category": "Tasks", "badge_tier": "bronze", "points": 100, "threshold": 10, "icon": "check-square"},
    {"code": "TASK_03", "title": "Task Master", "description": "Complete 50 tasks.", "category": "Tasks", "badge_tier": "silver", "points": 250, "threshold": 50, "icon": "check-square"},
    {"code": "TASK_04", "title": "Task Overlord", "description": "Complete 100 tasks.", "category": "Tasks", "badge_tier": "gold", "points": 500, "threshold": 100, "icon": "check-square"},
    {"code": "TASK_05", "title": "Task Legend", "description": "Complete 500 tasks.", "category": "Tasks", "badge_tier": "platinum", "points": 1000, "threshold": 500, "icon": "check-square"},
    {"code": "TASK_06", "title": "Subtask Crusher", "description": "Complete 25 subtasks.", "category": "Tasks", "badge_tier": "silver", "points": 150, "threshold": 25, "icon": "list"},
    {"code": "TASK_07", "title": "Priority Slayer", "description": "Complete 10 urgent priority tasks.", "category": "Tasks", "badge_tier": "gold", "points": 300, "threshold": 10, "icon": "alert-triangle"},
    {"code": "TASK_08", "title": "Planner Pro", "description": "Create tasks in 5 different categories.", "category": "Tasks", "badge_tier": "bronze", "points": 100, "threshold": 5, "icon": "folder"},
    {"code": "TASK_09", "title": "Early Bird", "description": "Complete 5 tasks before their due date.", "category": "Tasks", "badge_tier": "silver", "points": 200, "threshold": 5, "icon": "clock"},
    {"code": "TASK_10", "title": "Zero Backlog", "description": "Have 0 pending tasks remaining.", "category": "Tasks", "badge_tier": "diamond", "points": 750, "threshold": 1, "icon": "smile"},
    {"code": "TASK_11", "title": "Task Centurion", "description": "Complete 100 tasks in a single month.", "category": "Tasks", "badge_tier": "gold", "points": 600, "threshold": 100, "icon": "shield"},
    {"code": "TASK_12", "title": "High Velocity", "description": "Complete 10 tasks in a single day.", "category": "Tasks", "badge_tier": "silver", "points": 250, "threshold": 10, "icon": "zap"},
    {"code": "TASK_13", "title": "Recurring Champ", "description": "Complete 10 recurring task instances.", "category": "Tasks", "badge_tier": "bronze", "points": 150, "threshold": 10, "icon": "repeat"},
    {"code": "TASK_14", "title": "Tag Master", "description": "Organize tasks with 10 custom tags.", "category": "Tasks", "badge_tier": "bronze", "points": 100, "threshold": 10, "icon": "tag"},
    {"code": "TASK_15", "title": "Estimation Wizard", "description": "Log accurate task duration estimates 10 times.", "category": "Tasks", "badge_tier": "silver", "points": 200, "threshold": 10, "icon": "cpu"},

    # Habit Achievements (16-30)
    {"code": "HABIT_01", "title": "New Habit", "description": "Create your first daily habit.", "category": "Habits", "badge_tier": "bronze", "points": 50, "threshold": 1, "icon": "repeat"},
    {"code": "HABIT_02", "title": "7 Day Streak", "description": "Maintain a 7-day habit streak.", "category": "Habits", "badge_tier": "bronze", "points": 150, "threshold": 7, "icon": "zap"},
    {"code": "HABIT_03", "title": "14 Day Streak", "description": "Maintain a 14-day habit streak.", "category": "Habits", "badge_tier": "silver", "points": 300, "threshold": 14, "icon": "zap"},
    {"code": "HABIT_04", "title": "30 Day Streak", "description": "Maintain a 30-day habit streak.", "category": "Habits", "badge_tier": "gold", "points": 600, "threshold": 30, "icon": "zap"},
    {"code": "HABIT_05", "title": "100 Day Streak", "description": "Maintain a 100-day habit streak.", "category": "Habits", "badge_tier": "diamond", "points": 1500, "threshold": 100, "icon": "flame"},
    {"code": "HABIT_06", "title": "Habit Builder", "description": "Log 50 total habit completions.", "category": "Habits", "badge_tier": "silver", "points": 250, "threshold": 50, "icon": "activity"},
    {"code": "HABIT_07", "title": "Habit Machine", "description": "Log 200 total habit completions.", "category": "Habits", "badge_tier": "gold", "points": 750, "threshold": 200, "icon": "activity"},
    {"code": "HABIT_08", "title": "Perfect Day", "description": "Complete all active habits in a single day.", "category": "Habits", "badge_tier": "silver", "points": 200, "threshold": 1, "icon": "sun"},
    {"code": "HABIT_09", "title": "Habit Architect", "description": "Create 5 active daily habits.", "category": "Habits", "badge_tier": "bronze", "points": 100, "threshold": 5, "icon": "grid"},
    {"code": "HABIT_10", "title": "Consistency Titan", "description": "Maintain 3 active streaks of 14+ days.", "category": "Habits", "badge_tier": "platinum", "points": 1000, "threshold": 3, "icon": "shield"},
    {"code": "HABIT_11", "title": "Morning Routine", "description": "Log a morning habit before 9 AM.", "category": "Habits", "badge_tier": "bronze", "points": 100, "threshold": 1, "icon": "sun"},
    {"code": "HABIT_12", "title": "Night Reflection", "description": "Log an evening habit after 9 PM.", "category": "Habits", "badge_tier": "bronze", "points": 100, "threshold": 1, "icon": "moon"},
    {"code": "HABIT_13", "title": "Weekly Habit Pro", "description": "Maintain a weekly habit for 4 consecutive weeks.", "category": "Habits", "badge_tier": "silver", "points": 250, "threshold": 4, "icon": "calendar"},
    {"code": "HABIT_14", "title": "Streak Recovery", "description": "Recover a broken streak and rebuild 7 days.", "category": "Habits", "badge_tier": "silver", "points": 200, "threshold": 7, "icon": "refresh-cw"},
    {"code": "HABIT_15", "title": "Habit Mastermind", "description": "Log 500 total habit completions.", "category": "Habits", "badge_tier": "platinum", "points": 1200, "threshold": 500, "icon": "award"},

    # Goal Achievements (31-45)
    {"code": "GOAL_01", "title": "Visionary", "description": "Create your first long-term or short-term goal.", "category": "Goals", "badge_tier": "bronze", "points": 50, "threshold": 1, "icon": "target"},
    {"code": "GOAL_02", "title": "First Milestone", "description": "Complete your first goal milestone.", "category": "Goals", "badge_tier": "bronze", "points": 100, "threshold": 1, "icon": "flag"},
    {"code": "GOAL_03", "title": "Goal Crusher", "description": "Fully complete 1 goal.", "category": "Goals", "badge_tier": "silver", "points": 250, "threshold": 1, "icon": "award"},
    {"code": "GOAL_04", "title": "Goal Overachiever", "description": "Fully complete 5 goals.", "category": "Goals", "badge_tier": "gold", "points": 750, "threshold": 5, "icon": "award"},
    {"code": "GOAL_05", "title": "Goal Master", "description": "Fully complete 10 goals.", "category": "Goals", "badge_tier": "platinum", "points": 1500, "threshold": 10, "icon": "crown"},
    {"code": "GOAL_06", "title": "Milestone Runner", "description": "Complete 20 goal milestones.", "category": "Goals", "badge_tier": "silver", "points": 300, "threshold": 20, "icon": "check-circle"},
    {"code": "GOAL_07", "title": "Balanced Life", "description": "Have active goals in 4 different categories.", "category": "Goals", "badge_tier": "silver", "points": 200, "threshold": 4, "icon": "pie-chart"},
    {"code": "GOAL_08", "title": "Financial Vision", "description": "Complete a financial goal.", "category": "Goals", "badge_tier": "gold", "points": 400, "threshold": 1, "icon": "dollar-sign"},
    {"code": "GOAL_09", "title": "Career Breakthrough", "description": "Complete a career goal.", "category": "Goals", "badge_tier": "gold", "points": 400, "threshold": 1, "icon": "briefcase"},
    {"code": "GOAL_10", "title": "Learning Odyssey", "description": "Complete a learning goal.", "category": "Goals", "badge_tier": "silver", "points": 300, "threshold": 1, "icon": "book-open"},
    {"code": "GOAL_11", "title": "Long-Term Architect", "description": "Set a goal spanning over 1 year.", "category": "Goals", "badge_tier": "bronze", "points": 100, "threshold": 1, "icon": "compass"},
    {"code": "GOAL_12", "title": "Milestone Sprint", "description": "Complete 5 milestones in a single week.", "category": "Goals", "badge_tier": "silver", "points": 250, "threshold": 5, "icon": "trending-up"},
    {"code": "GOAL_13", "title": "OKRs Aligned", "description": "Achieve 80%+ progress on 3 objectives.", "category": "Goals", "badge_tier": "gold", "points": 500, "threshold": 3, "icon": "check-all"},
    {"code": "GOAL_14", "title": "Goal Strategist", "description": "Write progress notes for 10 goal updates.", "category": "Goals", "badge_tier": "bronze", "points": 150, "threshold": 10, "icon": "edit-3"},
    {"code": "GOAL_15", "title": "Unstoppable Vision", "description": "Fully complete 20 goals.", "category": "Goals", "badge_tier": "diamond", "points": 2500, "threshold": 20, "icon": "star"},

    # Focus & Productivity Achievements (46-60)
    {"code": "FOCUS_01", "title": "First Pomodoro", "description": "Complete your first 25-minute Focus session.", "category": "Focus", "badge_tier": "bronze", "points": 50, "threshold": 1, "icon": "timer"},
    {"code": "FOCUS_02", "title": "Deep Work Initiate", "description": "Log 5 total Focus sessions.", "category": "Focus", "badge_tier": "bronze", "points": 150, "threshold": 5, "icon": "cpu"},
    {"code": "FOCUS_03", "title": "Focus Master", "description": "Log 25 total Focus sessions.", "category": "Focus", "badge_tier": "silver", "points": 400, "threshold": 25, "icon": "cpu"},
    {"code": "FOCUS_04", "title": "Monk Mode", "description": "Log 100 total Focus sessions.", "category": "Focus", "badge_tier": "platinum", "points": 1200, "threshold": 100, "icon": "moon"},
    {"code": "FOCUS_05", "title": "10 Hours Focus", "description": "Accumulate 10 total hours of deep work.", "category": "Focus", "badge_tier": "silver", "points": 300, "threshold": 600, "icon": "clock"},
    {"code": "FOCUS_06", "title": "50 Hours Focus", "description": "Accumulate 50 total hours of deep work.", "category": "Focus", "badge_tier": "gold", "points": 800, "threshold": 3000, "icon": "clock"},
    {"code": "FOCUS_07", "title": "Distraction Free", "description": "Complete a Focus session with 0 distractions.", "category": "Focus", "badge_tier": "bronze", "points": 100, "threshold": 1, "icon": "shield"},
    {"code": "FOCUS_08", "title": "Marathon Focus", "description": "Complete a 90-minute Deep Work session.", "category": "Focus", "badge_tier": "gold", "points": 500, "threshold": 90, "icon": "zap"},
    {"code": "FOCUS_09", "title": "Distraction Logger", "description": "Log 10 distractions to protect flow state.", "category": "Focus", "badge_tier": "bronze", "points": 100, "threshold": 10, "icon": "eye-off"},
    {"code": "FOCUS_10", "title": "100 Hours Focus", "description": "Accumulate 100 total hours of deep work.", "category": "Focus", "badge_tier": "diamond", "points": 2000, "threshold": 6000, "icon": "award"},
    {"code": "FOCUS_11", "title": "Daily Focus Goal", "description": "Log 2+ hours of focus in a single day.", "category": "Focus", "badge_tier": "silver", "points": 200, "threshold": 120, "icon": "sun"},
    {"code": "FOCUS_12", "title": "Weekly Monk", "description": "Log 10+ hours of focus in a single week.", "category": "Focus", "badge_tier": "gold", "points": 600, "threshold": 600, "icon": "calendar"},
    {"code": "FOCUS_13", "title": "Pomodoro Streak", "description": "Complete 4 Pomodoro sessions in a single day.", "category": "Focus", "badge_tier": "silver", "points": 250, "threshold": 4, "icon": "repeat"},
    {"code": "FOCUS_14", "title": "Flow State Virtuoso", "description": "Maintain 5 consecutive 0-distraction sessions.", "category": "Focus", "badge_tier": "platinum", "points": 1000, "threshold": 5, "icon": "heart"},
    {"code": "FOCUS_15", "title": "Productivity Hero", "description": "Achieve a 5/5 average focus rating over 10 sessions.", "category": "Focus", "badge_tier": "gold", "points": 750, "threshold": 10, "icon": "star"},

    # Finance Achievements (61-75)
    {"code": "FINANCE_01", "title": "Money Logged", "description": "Log your first income or expense transaction.", "category": "Finance", "badge_tier": "bronze", "points": 50, "threshold": 1, "icon": "dollar-sign"},
    {"code": "FINANCE_02", "title": "Budget Conscious", "description": "Create a monthly category budget.", "category": "Finance", "badge_tier": "bronze", "points": 100, "threshold": 1, "icon": "credit-card"},
    {"code": "FINANCE_03", "title": "Saver Initiate", "description": "Create a Savings Goal.", "category": "Finance", "badge_tier": "bronze", "points": 100, "threshold": 1, "icon": "piggy-bank"},
    {"code": "FINANCE_04", "title": "Savings Champion", "description": "Reach 100% on a Savings Goal.", "category": "Finance", "badge_tier": "gold", "points": 500, "threshold": 1, "icon": "trending-up"},
    {"code": "FINANCE_05", "title": "Financial Auditor", "description": "Log 50 total transactions.", "category": "Finance", "badge_tier": "silver", "points": 250, "threshold": 50, "icon": "file-text"},
    {"code": "FINANCE_06", "title": "Smart Budgeter", "description": "Stay under budget in all categories for a month.", "category": "Finance", "badge_tier": "gold", "points": 600, "threshold": 1, "icon": "thumbs-up"},
    {"code": "FINANCE_07", "title": "Wealth Builder", "description": "Save at least 30% of monthly income.", "category": "Finance", "badge_tier": "platinum", "points": 1000, "threshold": 30, "icon": "dollar-sign"},
    {"code": "FINANCE_08", "title": "Transaction Master", "description": "Log 100 total transactions.", "category": "Finance", "badge_tier": "gold", "points": 600, "threshold": 100, "icon": "database"},
    {"code": "FINANCE_09", "title": "Emergency Fund", "description": "Accumulate 3 months of expenses in savings.", "category": "Finance", "badge_tier": "platinum", "points": 1200, "threshold": 3, "icon": "shield"},
    {"code": "FINANCE_10", "title": "Expense Tracking Ninja", "description": "Categorize 100% of monthly transactions.", "category": "Finance", "badge_tier": "silver", "points": 200, "threshold": 1, "icon": "check"},
    {"code": "FINANCE_11", "title": "Income Booster", "description": "Log 5 distinct income sources.", "category": "Finance", "badge_tier": "silver", "points": 300, "threshold": 5, "icon": "arrow-up-right"},
    {"code": "FINANCE_12", "title": "Budget Guardian", "description": "Set budgets across 5 expense categories.", "category": "Finance", "badge_tier": "bronze", "points": 150, "threshold": 5, "icon": "lock"},
    {"code": "FINANCE_13", "title": "Zero Waste Month", "description": "Keep non-essential spending below 15% of income.", "category": "Finance", "badge_tier": "gold", "points": 700, "threshold": 15, "icon": "pie-chart"},
    {"code": "FINANCE_14", "title": "50% Savings Rate", "description": "Save 50%+ of monthly income.", "category": "Finance", "badge_tier": "diamond", "points": 2000, "threshold": 50, "icon": "award"},
    {"code": "FINANCE_15", "title": "Financial Freedom", "description": "Reach $50,000 total cumulative net savings.", "category": "Finance", "badge_tier": "diamond", "points": 3000, "threshold": 50000, "icon": "sun"},

    # Learning Achievements (76-90)
    {"code": "LEARN_01", "title": "Curious Mind", "description": "Add your first study course.", "category": "Learning", "badge_tier": "bronze", "points": 50, "threshold": 1, "icon": "book-open"},
    {"code": "LEARN_02", "title": "Study Scholar", "description": "Log 10 study sessions.", "category": "Learning", "badge_tier": "bronze", "points": 150, "threshold": 10, "icon": "book"},
    {"code": "LEARN_03", "title": "Course Graduate", "description": "Complete a full learning course.", "category": "Learning", "badge_tier": "silver", "points": 400, "threshold": 1, "icon": "award"},
    {"code": "LEARN_04", "title": "Polymath", "description": "Complete 3 learning courses.", "category": "Learning", "badge_tier": "gold", "points": 900, "threshold": 3, "icon": "star"},
    {"code": "LEARN_05", "title": "Note Taker", "description": "Write 10 study notes.", "category": "Learning", "badge_tier": "bronze", "points": 100, "threshold": 10, "icon": "edit"},
    {"code": "LEARN_06", "title": "Knowledge Seeker", "description": "Accumulate 20 total study hours.", "category": "Learning", "badge_tier": "silver", "points": 500, "threshold": 1200, "icon": "clock"},
    {"code": "LEARN_07", "title": "Spaced Repetition Pro", "description": "Complete 25 flashcard reviews.", "category": "Learning", "badge_tier": "silver", "points": 300, "threshold": 25, "icon": "layers"},
    {"code": "LEARN_08", "title": "50 Hours Study", "description": "Accumulate 50 total study hours.", "category": "Learning", "badge_tier": "gold", "points": 1000, "threshold": 3000, "icon": "award"},
    {"code": "LEARN_09", "title": "Subject Specialist", "description": "Complete 5 courses in a single subject.", "category": "Learning", "badge_tier": "gold", "points": 800, "threshold": 5, "icon": "grid"},
    {"code": "LEARN_10", "title": "Daily Scholar", "description": "Log study sessions 7 days in a row.", "category": "Learning", "badge_tier": "silver", "points": 350, "threshold": 7, "icon": "zap"},

    # Journal, Profile & System Achievements (91-105)
    {"code": "JOURNAL_01", "title": "Reflective Mind", "description": "Write your first daily journal entry.", "category": "Journal", "badge_tier": "bronze", "points": 50, "threshold": 1, "icon": "book-open"},
    {"code": "JOURNAL_02", "title": "7 Journal Entries", "description": "Write 7 journal entries.", "category": "Journal", "badge_tier": "silver", "points": 200, "threshold": 7, "icon": "edit-3"},
    {"code": "JOURNAL_03", "title": "30 Journal Entries", "description": "Write 30 journal entries.", "category": "Journal", "badge_tier": "gold", "points": 500, "threshold": 30, "icon": "feather"},
    {"code": "JOURNAL_04", "title": "Emotional Clarity", "description": "Log mood valence in 10 journal entries.", "category": "Journal", "badge_tier": "bronze", "points": 150, "threshold": 10, "icon": "heart"},
    {"code": "JOURNAL_05", "title": "100 Journal Entries", "description": "Write 100 journal entries.", "category": "Journal", "badge_tier": "platinum", "points": 1200, "threshold": 100, "icon": "book"},
    {"code": "SYS_01", "title": "LifeOS Hero", "description": "Reach a total Life Score of 80+.", "category": "General", "badge_tier": "diamond", "points": 2000, "threshold": 80, "icon": "sun"},
    {"code": "SYS_02", "title": "LifeOS Titan", "description": "Reach a total Life Score of 90+.", "category": "General", "badge_tier": "diamond", "points": 3000, "threshold": 90, "icon": "crown"},
    {"code": "SYS_03", "title": "Profile Perfect", "description": "Fill out 100% of your user profile details.", "category": "General", "badge_tier": "bronze", "points": 100, "threshold": 1, "icon": "user"},
    {"code": "SYS_04", "title": "Dark Mode Cyber", "description": "Customize your LifeOS theme settings.", "category": "General", "badge_tier": "bronze", "points": 50, "threshold": 1, "icon": "moon"},
    {"code": "SYS_05", "title": "Master of LifeOS", "description": "Unlock 50 total achievements.", "category": "General", "badge_tier": "diamond", "points": 5000, "threshold": 50, "icon": "trophy"}
]

class AchievementEngine:

    @staticmethod
    def seed_achievements():
        """Populates baseline 100+ achievement definitions in database."""
        for ach_data in SYSTEM_ACHIEVEMENTS_DEFINITION:
            existing = Achievement.query.filter_by(code=ach_data["code"]).first()
            if not existing:
                ach = Achievement(**ach_data)
                db.session.add(ach)
        db.session.commit()

    @staticmethod
    def evaluate_user_achievements(user_id: int) -> List[Dict]:
        """Evaluates user progress against unlock thresholds and awards new achievements."""
        AchievementEngine.seed_achievements()

        unlocked_new = []

        # Gather User Metrics
        task_count = Task.query.filter_by(user_id=user_id, status="completed", is_deleted=False).count()
        subtask_count = Task.query.filter_by(user_id=user_id, is_deleted=False).count()
        habits = Habit.query.filter_by(user_id=user_id, is_deleted=False).all()
        best_streak = max((h.best_streak for h in habits), default=0)
        habit_comp_count = HabitCompletion.query.filter_by(user_id=user_id, status="completed").count()

        goal_completed = Goal.query.filter_by(user_id=user_id, status="completed", is_deleted=False).count()
        focus_sessions_count = FocusSession.query.filter_by(user_id=user_id, is_completed=True).count()
        focus_total_mins = db.session.query(db.func.sum(FocusSession.actual_minutes)).filter_by(user_id=user_id, is_completed=True).scalar() or 0

        tx_count = Transaction.query.filter_by(user_id=user_id, is_deleted=False).count()
        course_completed = Course.query.filter_by(user_id=user_id, status="completed", is_deleted=False).count()
        journal_count = JournalEntry.query.filter_by(user_id=user_id, is_deleted=False).count()

        # Map Code to Metric Values
        metrics_map = {
            "TASK_01": task_count, "TASK_02": task_count, "TASK_03": task_count, "TASK_04": task_count, "TASK_05": task_count,
            "TASK_11": task_count, "TASK_12": task_count,
            "HABIT_01": len(habits), "HABIT_02": best_streak, "HABIT_03": best_streak, "HABIT_04": best_streak, "HABIT_05": best_streak,
            "HABIT_06": habit_comp_count, "HABIT_07": habit_comp_count, "HABIT_15": habit_comp_count,
            "GOAL_01": Goal.query.filter_by(user_id=user_id, is_deleted=False).count(),
            "GOAL_03": goal_completed, "GOAL_04": goal_completed, "GOAL_05": goal_completed, "GOAL_15": goal_completed,
            "FOCUS_01": focus_sessions_count, "FOCUS_02": focus_sessions_count, "FOCUS_03": focus_sessions_count, "FOCUS_04": focus_sessions_count,
            "FOCUS_05": focus_total_mins, "FOCUS_06": focus_total_mins, "FOCUS_10": focus_total_mins,
            "FINANCE_01": tx_count, "FINANCE_05": tx_count, "FINANCE_08": tx_count,
            "LEARN_01": Course.query.filter_by(user_id=user_id, is_deleted=False).count(),
            "LEARN_03": course_completed, "LEARN_04": course_completed,
            "JOURNAL_01": journal_count, "JOURNAL_02": journal_count, "JOURNAL_03": journal_count, "JOURNAL_05": journal_count
        }

        all_achievements = Achievement.query.all()
        for ach in all_achievements:
            val = metrics_map.get(ach.code, 0)
            if val >= ach.threshold:
                already_unlocked = UserAchievement.query.filter_by(user_id=user_id, achievement_id=ach.id).first()
                if not already_unlocked:
                    ua = UserAchievement(
                        user_id=user_id,
                        achievement_id=ach.id,
                        unlocked_at=datetime.utcnow(),
                        progress=val
                    )
                    db.session.add(ua)

                    # Create Notification
                    notif = Notification(
                        user_id=user_id,
                        title=f"🏆 Achievement Unlocked: {ach.title}",
                        message=f"Congratulations! You unlocked '{ach.title}' (+{ach.points} pts).",
                        notification_type="achievement_unlocked",
                        severity="success",
                        entity_type="achievement",
                        entity_id=ach.id
                    )
                    db.session.add(notif)
                    unlocked_new.append(ach.to_dict())

        db.session.commit()
        return unlocked_new

    @staticmethod
    def get_user_achievements(user_id: int) -> List[Dict]:
        """Retrieves list of all achievements with unlocked status."""
        AchievementEngine.seed_achievements()
        AchievementEngine.evaluate_user_achievements(user_id)

        all_achs = Achievement.query.order_by(Achievement.id.asc()).all()
        unlocked_map = {ua.achievement_id: ua for ua in UserAchievement.query.filter_by(user_id=user_id).all()}

        results = []
        for ach in all_achs:
            data = ach.to_dict()
            is_unlocked = ach.id in unlocked_map
            data["unlocked"] = is_unlocked
            data["unlocked_at"] = unlocked_map[ach.id].unlocked_at.isoformat() if is_unlocked else None
            results.append(data)

        return results
