"""
Unit Test Suite for Journal & Sentiment Domain Service
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.journal_service import JournalService


class JournalServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='test_writer', email='writer@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_journal_entry(self):
        success, entry = JournalService.create_entry(self.user.id, {
            'title': 'Great Productive Day',
            'content': 'Today was an amazing, happy, and productive day full of accomplishments and flow state.',
            'mood': 'happy',
            'energy_level': 5
        })
        self.assertTrue(success)
        self.assertEqual(entry['title'], 'Great Productive Day')
        self.assertGreater(entry['valence_score'], 0.0)

    def test_mood_analytics(self):
        JournalService.create_entry(self.user.id, {
            'title': 'Entry 1',
            'content': 'Calm peaceful clear inspired day.',
            'mood': 'calm'
        })
        analytics = JournalService.get_mood_analytics(self.user.id)
        self.assertGreaterEqual(analytics['wellbeing_index'], 50.0)
