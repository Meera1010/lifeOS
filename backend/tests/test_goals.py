"""
LifeOS Automated Unit Tests — Goal Management
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.services.auth_service import AuthService
from backend.services.goal_service import GoalService

class GoalTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        ok, res = AuthService.register_user({
            "username": "goaluser",
            "email": "goal@example.com",
            "password": "Password123!"
        })
        self.user_id = res["user"]["id"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_and_milestone_goal(self):
        ok, goal = GoalService.create_goal(self.user_id, {
            "title": "Learn Italian Language",
            "category": "personal",
            "timeframe": "short_term",
            "milestones": [
                {"title": "Alphabet & Basics"},
                {"title": "Conversational Grammar"}
            ]
        })
        self.assertTrue(ok)
        self.assertEqual(len(goal["milestones"]), 2)
        self.assertEqual(goal["progress_percentage"], 0.0)

        # Toggle first milestone
        ms_id = goal["milestones"][0]["id"]
        ok, updated = GoalService.toggle_milestone(self.user_id, ms_id)
        self.assertTrue(ok)
        self.assertEqual(updated["progress_percentage"], 50.0)

if __name__ == "__main__":
    unittest.main()
