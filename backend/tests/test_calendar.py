"""
Unit Test Suite for Calendar Domain Service
"""

import unittest
from datetime import datetime, timedelta
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.calendar_service import CalendarService


class CalendarServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='test_cal_user', email='cal@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_event(self):
        start = (datetime.utcnow() + timedelta(hours=1)).isoformat()
        end = (datetime.utcnow() + timedelta(hours=2)).isoformat()

        success, event = CalendarService.create_event(self.user.id, {
            'title': 'System Design Review',
            'start_time': start,
            'end_time': end,
            'location': 'Conference Room A'
        })
        self.assertTrue(success)
        self.assertEqual(event['title'], 'System Design Review')

    def test_consolidated_calendar(self):
        now = datetime.utcnow()
        agenda = CalendarService.get_consolidated_calendar(self.user.id, now.year, now.month)
        self.assertEqual(agenda['year'], now.year)
        self.assertEqual(agenda['month'], now.month)
