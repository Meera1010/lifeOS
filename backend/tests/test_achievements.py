"""
LifeOS Automated Unit Tests — Achievement Engine
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.services.auth_service import AuthService
from backend.services.task_service import TaskService
from backend.services.achievement_engine import AchievementEngine

class AchievementTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        ok, res = AuthService.register_user({
            "username": "achuser",
            "email": "ach@example.com",
            "password": "Password123!"
        })
        self.user_id = res["user"]["id"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_achievement_seed_and_unlock(self):
        # Create completed task to trigger FIRST_TASK achievement
        TaskService.create_task(self.user_id, {"title": "Task 1", "status": "completed"})

        unlocked = AchievementEngine.evaluate_user_achievements(self.user_id)
        self.assertGreater(len(unlocked), 0)

        all_achs = AchievementEngine.get_user_achievements(self.user_id)
        self.assertGreaterEqual(len(all_achs), 50)

if __name__ == "__main__":
    unittest.main()
