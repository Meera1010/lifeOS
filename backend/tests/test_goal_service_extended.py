"""
Unit Test Suite for Goal Service Edge Cases & Milestones
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.goal_service import GoalService


class GoalServiceExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='goal_tester', email='goal_tester@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_and_toggle_milestone(self):
        success_g, goal = GoalService.create_goal(self.user.id, {
            'title': 'Publish Technical Book',
            'milestones': ['Outline', 'Chapter 1']
        })
        self.assertTrue(success_g)
        self.assertEqual(len(goal['milestones']), 2)

        ms_id = goal['milestones'][0]['id']
        success_m, updated_g = GoalService.toggle_milestone(self.user.id, ms_id)
        self.assertTrue(success_m)
        self.assertGreater(updated_g['progress_percentage'], 0.0)
