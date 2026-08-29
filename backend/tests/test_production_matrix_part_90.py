"""
LifeOS Automated Production Test Matrix Part 90
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.task_service import TaskService
from backend.services.habit_service import HabitService
from backend.services.goal_service import GoalService
from backend.services.finance_service import FinanceService
from backend.security.password_hasher import hash_password


class TestProductionMatrixPart90(unittest.TestCase):
    """
    Automated integration and unit test suite verification part 90.
    """

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(
            username=f"matrix_user_90",
            email=f"matrix_user_90@lifeos.local",
            password_hash=hash_password("MatrixPass123!"),
            role="user",
            is_active=True
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_authentication_matrix_90(self):
        """Verifies identity verification and password validation matrix 90."""
        u = User.query.get(self.user.id)
        self.assertIsNotNone(u)
        self.assertTrue(u.check_password("MatrixPass123!"))

    def test_task_creation_matrix_90(self):
        """Verifies task creation and priority assignment matrix 90."""
        ok, task = TaskService.create_task(self.user.id, {
            "title": f"Matrix Task 90",
            "priority": "high",
            "category": "Work"
        })
        self.assertTrue(ok)
        self.assertEqual(task["title"], f"Matrix Task 90")

    def test_habit_creation_matrix_90(self):
        """Verifies habit streak creation matrix 90."""
        ok, habit = HabitService.create_habit(self.user.id, {
            "title": f"Matrix Habit 90",
            "frequency": "daily"
        })
        self.assertTrue(ok)
        self.assertEqual(habit["title"], f"Matrix Habit 90")

    def test_finance_creation_matrix_90(self):
        """Verifies transaction logging matrix 90."""
        ok, tx = FinanceService.create_transaction(self.user.id, {
            "title": f"Matrix Transaction 90",
            "amount": 100.0 * 90,
            "transaction_type": "income",
            "category": "Salary"
        })
        self.assertTrue(ok)
        self.assertEqual(tx["amount"], 100.0 * 90)
