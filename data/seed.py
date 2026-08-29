"""
LifeOS Realistic Sample Data Seeder
"""

from datetime import datetime, date, timedelta
from backend.models.base import db
from backend.models.user import User, UserProfile, UserSession
from backend.models.task import Task, Subtask, TaskCategory, TaskTag
from backend.models.habit import Habit, HabitCompletion
from backend.models.goal import Goal, Milestone
from backend.models.calendar import CalendarEvent, EventCategory
from backend.models.finance import Transaction, FinanceCategory, Budget, SavingsGoal
from backend.models.learning import Subject, Course, StudySession, LearningNote
from backend.models.focus import FocusSession, PomodoroSetting, DailyFocusSummary
from backend.models.journal import JournalEntry, JournalTag, MoodTracker
from backend.models.achievement import Achievement
from backend.models.notification import Notification, NotificationPreference
from backend.models.settings import UserSettings, DashboardPreference
from backend.models.audit import AuditLog
from backend.app.constants import DEFAULT_TASK_CATEGORIES, DEFAULT_FINANCE_CATEGORIES
from backend.services.achievement_engine import AchievementEngine
from backend.security.password_hasher import hash_password

def seed_database_sample_data():
    """Seeds the SQLite database with comprehensive sample data if empty."""
    if User.query.first():
        # Database already seeded
        return

    print("Seeding LifeOS database with realistic sample data...")

    # 1. Admin User & Standard User
    admin = User(
        username="admin",
        email="admin@lifeos.local",
        password_hash=hash_password("AdminPass123!"),
        role="admin",
        is_active=True,
        is_verified=True
    )
    db.session.add(admin)
    db.session.flush()

    admin_profile = UserProfile(
        user_id=admin.id,
        full_name="System Administrator",
        bio="LifeOS System Admin & Platform Engineer",
        timezone="UTC"
    )
    db.session.add(admin_profile)
    db.session.add(UserSettings(user_id=admin.id))
    db.session.add(DashboardPreference(user_id=admin.id))
    db.session.add(NotificationPreference(user_id=admin.id))

    user = User(
        username="alex_dev",
        email="alex@lifeos.local",
        password_hash=hash_password("UserPass123!"),
        role="user",
        is_active=True,
        is_verified=True
    )
    db.session.add(user)
    db.session.flush()

    user_profile = UserProfile(
        user_id=user.id,
        full_name="Alex Morgan",
        bio="Full-Stack Engineer & Lifelong Learner pursuing peak productivity.",
        occupation="Software Engineer",
        location="San Francisco, CA",
        timezone="PST",
        life_motto="Kaizen — Continuous daily improvement."
    )
    db.session.add(user_profile)
    db.session.add(UserSettings(user_id=user.id))
    db.session.add(DashboardPreference(user_id=user.id))
    db.session.add(NotificationPreference(user_id=user.id))

    # 2. Categories
    task_cats = []
    for tc in DEFAULT_TASK_CATEGORIES:
        cat = TaskCategory(user_id=user.id, **tc)
        db.session.add(cat)
        task_cats.append(cat)
    db.session.flush()

    fin_cats = []
    for fc in DEFAULT_FINANCE_CATEGORIES:
        fcat = FinanceCategory(user_id=user.id, **fc)
        db.session.add(fcat)
        fin_cats.append(fcat)
    db.session.flush()

    # 3. Tasks & Subtasks
    tasks_data = [
        {"title": "Complete LifeOS Architecture Specification", "priority": "high", "status": "completed", "cat_idx": 0, "due": 1},
        {"title": "Review Q3 Personal Financial Budget", "priority": "urgent", "status": "pending", "cat_idx": 3, "due": 2},
        {"title": "Read 30 pages of Clean Architecture book", "priority": "medium", "status": "pending", "cat_idx": 4, "due": 3},
        {"title": "Weekly Grocery Shopping & Meal Prep", "priority": "medium", "status": "completed", "cat_idx": 5, "due": -1},
        {"title": "Schedule Annual Health Checkup", "priority": "low", "status": "pending", "cat_idx": 2, "due": 5}
    ]

    for td in tasks_data:
        t = Task(
            user_id=user.id,
            category_id=task_cats[td["cat_idx"]].id,
            title=td["title"],
            priority=td["priority"],
            status=td["status"],
            due_date=datetime.utcnow() + timedelta(days=td["due"]),
            estimated_minutes=45,
            actual_minutes=40 if td["status"] == "completed" else 0
        )
        db.session.add(t)
        db.session.flush()

        # Add Subtasks
        st1 = Subtask(task_id=t.id, title="Draft initial requirements", is_completed=True)
        st2 = Subtask(task_id=t.id, title="Finalize implementation plan", is_completed=(td["status"] == "completed"))
        db.session.add(st1)
        db.session.add(st2)

    # 4. Habits & Completions
    h1 = Habit(user_id=user.id, title="Morning Meditation & Mindful Breathing", category="Health", color="#10b981", frequency="daily", current_streak=12, best_streak=15)
    h2 = Habit(user_id=user.id, title="30 Minutes Daily Exercise & Cardio", category="Health", color="#ef4444", frequency="daily", current_streak=5, best_streak=21)
    h3 = Habit(user_id=user.id, title="Read Technical Documentation / Book", category="Education", color="#8b5cf6", frequency="daily", current_streak=8, best_streak=14)

    db.session.add(h1)
    db.session.add(h2)
    db.session.add(h3)
    db.session.flush()

    for i in range(14):
        d = date.today() - timedelta(days=i)
        db.session.add(HabitCompletion(habit_id=h1.id, user_id=user.id, completion_date=d, status="completed"))
        if i % 2 == 0:
            db.session.add(HabitCompletion(habit_id=h2.id, user_id=user.id, completion_date=d, status="completed"))

    # 5. Goals & Milestones
    g1 = Goal(
        user_id=user.id,
        title="Master Modern Web Application Architecture",
        category="career",
        timeframe="long_term",
        priority="high",
        target_date=datetime.utcnow() + timedelta(days=180),
        target_metric_value=100.0,
        current_metric_value=65.0,
        metric_unit="percentage",
        color="#4f46e5",
        progress_percentage=65.0
    )
    db.session.add(g1)
    db.session.flush()

    m1 = Milestone(goal_id=g1.id, title="Complete Flask Advanced Backend", is_completed=True)
    m2 = Milestone(goal_id=g1.id, title="Build Custom UI Design System", is_completed=True)
    m3 = Milestone(goal_id=g1.id, title="Deploy Production Deployment Suite", is_completed=False)
    db.session.add(m1)
    db.session.add(m2)
    db.session.add(m3)

    # 6. Finance Transactions & Budgets
    db.session.add(Transaction(user_id=user.id, category_id=fin_cats[0].id, type="income", amount=4500.0, description="Monthly Software Engineer Salary", transaction_date=date.today() - timedelta(days=5)))
    db.session.add(Transaction(user_id=user.id, category_id=fin_cats[3].id, type="expense", amount=1400.0, description="Apartment Rent Payment", transaction_date=date.today() - timedelta(days=4)))
    db.session.add(Transaction(user_id=user.id, category_id=fin_cats[4].id, type="expense", amount=120.0, description="Weekly Grocery Restock", transaction_date=date.today() - timedelta(days=2)))

    db.session.add(Budget(user_id=user.id, category_id=fin_cats[4].id, monthly_limit=500.0, year=date.today().year, month=date.today().month))
    db.session.add(SavingsGoal(user_id=user.id, title="Emergency Reserve Fund", target_amount=10000.0, current_amount=4500.0, color="#10b981"))

    # 7. Learning Courses & Study Sessions
    subj = Subject(user_id=user.id, name="Computer Science", color="#8b5cf6")
    db.session.add(subj)
    db.session.flush()

    course = Course(user_id=user.id, subject_id=subj.id, title="Distributed Systems & Database Internals", provider="Self-Study", total_modules=10, completed_modules=6, progress_percentage=60.0)
    db.session.add(course)
    db.session.flush()

    db.session.add(StudySession(user_id=user.id, course_id=course.id, subject_id=subj.id, title="SQLite B-Tree Indexing Deep Dive", duration_minutes=90, topics_covered="WAL Mode, Page Cache, B-Tree Nodes", comprehension_rating=5))

    # 8. Focus Sessions
    db.session.add(FocusSession(user_id=user.id, session_type="pomodoro", duration_minutes=25, actual_minutes=25, productivity_rating=5, distraction_count=0))
    db.session.add(FocusSession(user_id=user.id, session_type="deep_work", duration_minutes=50, actual_minutes=50, productivity_rating=4, distraction_count=1))
    db.session.add(PomodoroSetting(user_id=user.id))

    # 9. Journal Entries
    j1 = JournalEntry(user_id=user.id, title="Reflections on System Architecture & Daily Flow", content="Today was remarkably productive. Focusing on modular service architecture allowed deep flow state during development.", mood="great", energy_level=9)
    db.session.add(j1)

    # 10. Seed Achievements & Evaluate
    AchievementEngine.seed_achievements()
    AchievementEngine.evaluate_user_achievements(user.id)

    # 11. Initial Notifications & Audit Logs
    db.session.add(Notification(user_id=user.id, title="Welcome to LifeOS!", message="Your Personal Life Management & Analytics Platform is ready.", notification_type="system_alert", severity="info"))
    db.session.add(AuditLog(user_id=user.id, action="SYSTEM_INIT", resource_type="system", details="Database initialized with sample data."))

    db.session.commit()
    print("LifeOS sample data successfully seeded!")
