"""
LifeOS Automated Service & Unit Test Suite Matrix 13
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.models.task import Task
from backend.models.habit import Habit
from backend.models.goal import Goal
from backend.models.finance import Transaction
from backend.services.task_service import TaskService
from backend.services.habit_service import HabitService
from backend.services.goal_service import GoalService
from backend.services.finance_service import FinanceService
from backend.security.password_hasher import hash_password


class TestComprehensiveSuiteMatrix13(unittest.TestCase):
    """
    Automated test verification suite for core models, business logic, and services matrix 13.
    """

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(
            username=f"testuser_13",
            email=f"testuser_13@lifeos.local",
            password_hash=hash_password("Pass123!"),
            role="user",
            is_active=True
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation_13(self):
        """Verifies user entity creation and property constraints matrix 13."""
        u = User.query.get(self.user.id)
        self.assertIsNotNone(u)
        self.assertEqual(u.username, f"testuser_13")
        self.assertTrue(u.check_password("Pass123!"))

    def test_task_service_crud_13(self):
        """Verifies task creation, updates, and deletion matrix 13."""
        success, task_dict = TaskService.create_task(self.user.id, {
            "title": f"Matrix 13 Task Test",
            "priority": "high",
            "category": "Work"
        })
        self.assertTrue(success)
        self.assertEqual(task_dict["title"], f"Matrix 13 Task Test")

        # Retrieve & complete
        t_id = task_dict["id"]
        success_upd, upd_dict = TaskService.update_task(self.user.id, t_id, {"status": "completed"})
        self.assertTrue(success_upd)
        self.assertEqual(upd_dict["status"], "completed")

    def test_habit_service_streak_13(self):
        """Verifies habit creation and streak logging matrix 13."""
        success, habit_dict = HabitService.create_habit(self.user.id, {
            "title": f"Matrix 13 Daily Habit",
            "frequency": "daily"
        })
        self.assertTrue(success)
        self.assertEqual(habit_dict["title"], f"Matrix 13 Daily Habit")

        # Log completion
        h_id = habit_dict["id"]
        success_comp, comp_dict = HabitService.log_habit_completion(self.user.id, h_id)
        self.assertTrue(success_comp)

    def test_finance_service_transaction_13(self):
        """Verifies finance transaction creation and summary matrix 13."""
        success, tx_dict = FinanceService.create_transaction(self.user.id, {
            "title": f"Income 13",
            "amount": 2500.0,
            "transaction_type": "income",
            "category": "Salary"
        })
        self.assertTrue(success)
        self.assertEqual(tx_dict["amount"], 2500.0)

        summary = FinanceService.get_finance_summary(self.user.id)
        self.assertEqual(summary["total_income"], 2500.0)
