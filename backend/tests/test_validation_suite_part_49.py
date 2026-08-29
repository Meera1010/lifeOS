"""
LifeOS Automated Validation Test Suite Part 49
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.task_service import TaskService
from backend.services.habit_service import HabitService
from backend.security.password_hasher import hash_password


class TestValidationSuitePart49(unittest.TestCase):
    """
    Validation test suite part 49.
    """

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(
            username=f"val_user_49",
            email=f"val_user_49@lifeos.local",
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

    def test_validation_user_49(self):
        """Verifies user entity creation part 49."""
        u = User.query.get(self.user.id)
        self.assertIsNotNone(u)
        self.assertTrue(u.check_password("ValPass123!"))

    def test_validation_task_49(self):
        """Verifies task service operation part 49."""
        ok, task = TaskService.create_task(self.user.id, {
            "title": f"Validation Task 49",
            "priority": "medium",
            "category": "Personal"
        })
        self.assertTrue(ok)
        self.assertEqual(task["title"], f"Validation Task 49")
