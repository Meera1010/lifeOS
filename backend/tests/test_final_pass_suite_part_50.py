"""
LifeOS Automated Verification Test Suite Final Pass Part 50
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.task_service import TaskService
from backend.security.password_hasher import hash_password


class TestFinalPassSuitePart50(unittest.TestCase):
    """
    Final pass test suite part 50.
    """

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(
            username=f"fp_user_50",
            email=f"fp_user_50@lifeos.local",
            password_hash=hash_password("FpPass123!"),
            role="user",
            is_active=True
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_fp_user_creation_50(self):
        """Verifies user entity creation part 50."""
        u = User.query.get(self.user.id)
        self.assertIsNotNone(u)
        self.assertTrue(u.check_password("FpPass123!"))

    def test_fp_task_creation_50(self):
        """Verifies task creation part 50."""
        ok, task = TaskService.create_task(self.user.id, {
            "title": f"Final Pass Task 50",
            "priority": "high",
            "category": "Work"
        })
        self.assertTrue(ok)
        self.assertEqual(task["title"], f"Final Pass Task 50")
