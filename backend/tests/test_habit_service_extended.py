"""
Unit Test Suite for Habit Service Edge Cases & Matrix Data
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.habit_service import HabitService


class HabitServiceExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='habit_tester', email='habit_tester@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_habit_calendar_matrix(self):
        HabitService.create_habit(self.user.id, {'title': 'Morning Meditation'})
        matrix = HabitService.get_habit_calendar_data(self.user.id, days=7)
        self.assertEqual(len(matrix['dates']), 7)
        self.assertIn('matrix', matrix)

    def test_habit_statistics(self):
        HabitService.create_habit(self.user.id, {'title': 'Daily Run'})
        stats = HabitService.get_habit_statistics(self.user.id)
        self.assertEqual(stats['total_habits'], 1)
