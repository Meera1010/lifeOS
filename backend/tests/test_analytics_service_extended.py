"""
Unit Test Suite for Executive Analytics Service & Dashboard
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.analytics_service import AnalyticsService


class AnalyticsServiceExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='analytics_user', email='analytics@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_executive_dashboard(self):
        dash = AnalyticsService.get_executive_dashboard(self.user.id)
        self.assertIn('life_score', dash)
        self.assertIn('smart_insights', dash)
        self.assertIn('summary_cards', dash)
        self.assertIn('charts', dash)
