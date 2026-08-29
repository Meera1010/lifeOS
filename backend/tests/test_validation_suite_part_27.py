"""
LifeOS Automated Validation Test Suite Part 27
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.task_service import TaskService
from backend.services.habit_service import HabitService
from backend.security.password_hasher import hash_password


class TestValidationSuitePart27(unittest.TestCase):
    """
    Validation test suite part 27.
    """

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(
            username=f"val_user_27",
            email=f"val_user_27@lifeos.local",
            password_hash=hash_password("ValPass123!"),
            role="user",
            is_active=True
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_validation_user_27(self):
        """Verifies user entity creation part 27."""
        u = User.query.get(self.user.id)
        self.assertIsNotNone(u)
        self.assertTrue(u.check_password("ValPass123!"))

    def test_validation_task_27(self):
        """Verifies task service operation part 27."""
        ok, task = TaskService.create_task(self.user.id, {
            "title": f"Validation Task 27",
            "priority": "medium",
            "category": "Personal"
        })
        self.assertTrue(ok)
        self.assertEqual(task["title"], f"Validation Task 27")
