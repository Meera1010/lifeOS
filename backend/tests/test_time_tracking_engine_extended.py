"""
Unit Test Suite for Time Allocation & Interruption Cost Engine
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.time_tracking_engine import TimeTrackingEngine


class TimeTrackingEngineExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='time_user', email='time@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_time_efficiency_index(self):
        res = TimeTrackingEngine.calculate_time_efficiency_index(self.user.id)
        self.assertIn('estimated_hours', res)
        self.assertIn('actual_hours', res)
        self.assertIn('estimation_variance_percentage', res)
