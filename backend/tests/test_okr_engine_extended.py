"""
Unit Test Suite for OKR Alignment Engine
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.okr_engine import OKREngine


class OKREngineExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='okr_user', email='okr@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_okr_alignment_calculation(self):
        res = OKREngine.calculate_okr_alignment(self.user.id)
        self.assertIn('overall_alignment_score', res)
        self.assertIn('objectives', res)
