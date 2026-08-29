"""
Unit Test Suite for Habit Models and Streaks
"""

import unittest
from datetime import date, timedelta
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.models.habit import Habit, HabitCompletion


class HabitModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='habit_model_user', email='habit_model@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_habit_streak_calculation(self):
        habit = Habit(user_id=self.user.id, title='Read Books', frequency='daily')
        db.session.add(habit)
        db.session.flush()

        c1 = HabitCompletion(habit_id=habit.id, user_id=self.user.id, completion_date=date.today(), status='completed')
        db.session.add(c1)
        db.session.commit()

        habit.update_streak_counts()
        self.assertEqual(habit.current_streak, 1)
