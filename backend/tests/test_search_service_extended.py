"""
Unit Test Suite for Global Full-Text Search Engine
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.task_service import TaskService
from backend.services.search_service import SearchService


class SearchServiceExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='search_user', email='search@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_global_search(self):
        TaskService.create_task(self.user.id, {'title': 'Quantum Physics Study Notes'})
        res = SearchService.global_search(self.user.id, 'Quantum')
        self.assertIn('results', res)
        self.assertGreaterEqual(len(res['results']), 1)
        self.assertEqual(res['results'][0]['title'], 'Quantum Physics Study Notes')
