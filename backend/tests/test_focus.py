"""
Unit Test Suite for Focus & Pomodoro Domain Service
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.focus_service import FocusService


class FocusServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='test_focus_user', email='focus@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_start_and_complete_focus_session(self):
        success, session = FocusService.start_focus_session(self.user.id, {
            'target_minutes': 25,
            'session_type': 'pomodoro'
        })
        self.assertTrue(success)
        self.assertFalse(session['is_completed'])

        success_comp, completed_session = FocusService.complete_focus_session(self.user.id, session['id'], {
            'actual_minutes': 25,
            'focus_rating': 5,
            'notes': 'Great deep work session!'
        })
        self.assertTrue(success_comp)
        self.assertTrue(completed_session['is_completed'])
        self.assertEqual(completed_session['productivity_rating'], 5)

    def test_log_distraction(self):
        _, session = FocusService.start_focus_session(self.user.id, {'target_minutes': 25})
        success, updated = FocusService.log_distraction(self.user.id, session['id'], 'Phone call')
        self.assertTrue(success)
        self.assertEqual(updated['distraction_count'], 1)
