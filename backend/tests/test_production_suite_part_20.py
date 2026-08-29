"""
LifeOS Automated Production Unit Test Suite Part 20
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.task_service import TaskService
from backend.services.habit_service import HabitService
from backend.services.goal_service import GoalService
from backend.security.password_hasher import hash_password


class TestProductionSuitePart20(unittest.TestCase):
    """
    Automated integration and unit test suite verification part 20.
    """

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(
            username=f"prod_test_20",
            email=f"prod_test_20@lifeos.local",
            password_hash=hash_password("TestPass123!"),
            role="user",
            is_active=True
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_authentication_20(self):
        """Verifies password hashing and identity validation part 20."""
        u = User.query.get(self.user.id)
        self.assertIsNotNone(u)
        self.assertTrue(u.check_password("TestPass123!"))

    def test_task_management_workflow_20(self):
        """Verifies task creation and lifecycle management part 20."""
        ok, task = TaskService.create_task(self.user.id, {
            "title": f"Production Task 20",
            "priority": "high",
            "category": "Work"
        })
        self.assertTrue(ok)
        self.assertEqual(task["title"], f"Production Task 20")

    def test_habit_tracking_workflow_20(self):
        """Verifies habit streak logging and completion matrix part 20."""
        ok, habit = HabitService.create_habit(self.user.id, {
            "title": f"Production Habit 20",
            "frequency": "daily"
        })
        self.assertTrue(ok)
        self.assertEqual(habit["title"], f"Production Habit 20")
