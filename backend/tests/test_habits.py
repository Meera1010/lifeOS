"""
LifeOS Automated Unit Tests — Habit Tracker
"""

import unittest
from datetime import date, timedelta
from backend.app import create_app
from backend.models.base import db
from backend.services.auth_service import AuthService
from backend.services.habit_service import HabitService

class HabitTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        ok, res = AuthService.register_user({
            "username": "habituser",
            "email": "habit@example.com",
            "password": "Password123!"
        })
        self.user_id = res["user"]["id"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_and_toggle_habit(self):
        ok, habit = HabitService.create_habit(self.user_id, {
            "title": "Daily Meditation",
            "category": "Health",
            "frequency": "daily"
        })
        self.assertTrue(ok)
        self.assertEqual(habit["title"], "Daily Meditation")

        # Toggle completion today
        ok, res = HabitService.toggle_habit_completion(self.user_id, habit["id"])
        self.assertTrue(ok)
        self.assertEqual(res["current_streak"], 1)

    def test_habit_streak_calculation(self):
        ok, habit = HabitService.create_habit(self.user_id, {"title": "Exercise"})
        h_id = habit["id"]

        # Log completion for yesterday and today
        yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        HabitService.toggle_habit_completion(self.user_id, h_id, target_date_str=yesterday)
        ok, res = HabitService.toggle_habit_completion(self.user_id, h_id)
        self.assertEqual(res["current_streak"], 2)

if __name__ == "__main__":
    unittest.main()
