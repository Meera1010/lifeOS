"""
LifeOS Test Suite Generator — Builds comprehensive automated unit tests
for all domain services, engines, security validators, and model mixins.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def write_file(rel_path, content):
    abs_path = os.path.join(PROJECT_ROOT, rel_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_test_learning():
    code = '''"""
Unit Test Suite for Learning & Course Domain Service
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.learning_service import LearningService


class LearningServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='test_learner', email='learner@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_course(self):
        success, course = LearningService.create_course(self.user.id, {
            'title': 'Advanced Python Systems Architecture',
            'instructor': 'Guido',
            'estimated_hours': 20.0
        })
        self.assertTrue(success)
        self.assertEqual(course['title'], 'Advanced Python Systems Architecture')
        self.assertEqual(course['progress_percentage'], 0.0)

    def test_log_study_session(self):
        _, course = LearningService.create_course(self.user.id, {
            'title': 'Flask Mastery',
            'estimated_hours': 10.0
        })
        success, session = LearningService.log_study_session(self.user.id, {
            'course_id': course['id'],
            'duration_minutes': 120,
            'topics_covered': 'Application Factory & Blueprints'
        })
        self.assertTrue(success)
        self.assertEqual(session['duration_minutes'], 120)

        analytics = LearningService.get_learning_analytics(self.user.id)
        self.assertEqual(analytics['monthly_study_hours'], 2.0)
'''
    write_file("backend/tests/test_learning.py", code)

def generate_test_focus():
    code = '''"""
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
        self.assertEqual(completed_session['focus_rating'], 5)

    def test_log_distraction(self):
        _, session = FocusService.start_focus_session(self.user.id, {'target_minutes': 25})
        success, updated = FocusService.log_distraction(self.user.id, session['id'], 'Phone call')
        self.assertTrue(success)
        self.assertEqual(updated['distraction_count'], 1)
'''
    write_file("backend/tests/test_focus.py", code)

def generate_test_journal():
    code = '''"""
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
'''
    write_file("backend/tests/test_journal.py", code)

def generate_test_calendar():
    code = '''"""
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
'''
    write_file("backend/tests/test_calendar.py", code)

def generate_test_engines():
    code = '''"""
Unit Test Suite for Domain Algorithmic Engines
"""

import unittest
from backend.services.spaced_repetition_engine import SpacedRepetitionEngine
from backend.services.sentiment_engine import SentimentEngine


class EnginesTestCase(unittest.TestCase):

    def test_spaced_repetition_sm2(self):
        reps, interval, ef, next_date = SpacedRepetitionEngine.calculate_next_review(
            quality_rating=5,
            repetition_count=0,
            interval_days=1,
            easiness_factor=2.5
        )
        self.assertEqual(reps, 1)
        self.assertEqual(interval, 1)
        self.assertGreaterEqual(ef, 2.5)

    def test_sentiment_engine(self):
        res_pos = SentimentEngine.analyze_text_sentiment("Amazing, happy, productive, flow state!")
        self.assertEqual(res_pos['sentiment'], 'positive')
        self.assertGreater(res_pos['valence_score'], 0.0)

        res_neg = SentimentEngine.analyze_text_sentiment("Stressed, exhausted, overwhelmed, failure.")
        self.assertEqual(res_neg['sentiment'], 'negative')
        self.assertLess(res_neg['valence_score'], 0.0)
'''
    write_file("backend/tests/test_engines.py", code)

def main():
    print("Generating comprehensive test suites...")
    generate_test_learning()
    generate_test_focus()
    generate_test_journal()
    generate_test_calendar()
    generate_test_engines()
    print("Test suites generated.")

if __name__ == "__main__":
    main()
