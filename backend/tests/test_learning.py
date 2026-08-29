"""
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
