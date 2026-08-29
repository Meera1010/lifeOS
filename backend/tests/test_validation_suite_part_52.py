"""
LifeOS Automated Validation Test Suite Part 52
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.task_service import TaskService
from backend.services.habit_service import HabitService
from backend.security.password_hasher import hash_password


class TestValidationSuitePart52(unittest.TestCase):
    """
    Validation test suite part 52.
    """

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(
            username=f"val_user_52",
            email=f"val_user_52@lifeos.local",
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

    def test_validation_user_52(self):
        """Verifies user entity creation part 52."""
        u = User.query.get(self.user.id)
        self.assertIsNotNone(u)
        self.assertTrue(u.check_password("ValPass123!"))

    def test_validation_task_52(self):
        """Verifies task service operation part 52."""
        ok, task = TaskService.create_task(self.user.id, {
            "title": f"Validation Task 52",
            "priority": "medium",
            "category": "Personal"
        })
        self.assertTrue(ok)
        self.assertEqual(task["title"], f"Validation Task 52")
