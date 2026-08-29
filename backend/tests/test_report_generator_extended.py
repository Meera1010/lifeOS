"""
Unit Test Suite for Executive Markdown Report Generator
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.report_generator import ReportGenerator


class ReportGeneratorExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='report_user', email='report@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_generate_weekly_report(self):
        report_md = ReportGenerator.generate_weekly_report_markdown(self.user.id)
        self.assertIn('# 📊 LifeOS Executive Weekly Performance Report', report_md)
        self.assertIn('Overall Life Score', report_md)
