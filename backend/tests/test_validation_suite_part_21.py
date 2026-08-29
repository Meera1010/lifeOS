"""
LifeOS Automated Validation Test Suite Part 21
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.task_service import TaskService
from backend.services.habit_service import HabitService
from backend.security.password_hasher import hash_password


class TestValidationSuitePart21(unittest.TestCase):
    """
    Validation test suite part 21.
    """

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(
            username=f"val_user_21",
            email=f"val_user_21@lifeos.local",
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

    def test_validation_user_21(self):
        """Verifies user entity creation part 21."""
        u = User.query.get(self.user.id)
        self.assertIsNotNone(u)
        self.assertTrue(u.check_password("ValPass123!"))

    def test_validation_task_21(self):
        """Verifies task service operation part 21."""
        ok, task = TaskService.create_task(self.user.id, {
            "title": f"Validation Task 21",
            "priority": "medium",
            "category": "Personal"
        })
        self.assertTrue(ok)
        self.assertEqual(task["title"], f"Validation Task 21")
