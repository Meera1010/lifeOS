"""
Integration Test Suite for Habits API Blueprint Routes
"""

import unittest
import json
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User


class HabitsRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='route_habit_user', email='route_habit@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

        res = self.client.post('/api/auth/login', json={'email': 'route_habit@example.com', 'password': 'Password123!'})
        self.token = json.loads(res.data)['data']['token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_habits_api_lifecycle(self):
        res_create = self.client.post('/api/habits', json={'title': 'API Route Habit'}, headers=self.headers)
        self.assertEqual(res_create.status_code, 201)
        habit_id = json.loads(res_create.data)['data']['id']

        res_toggle = self.client.post(f'/api/habits/{habit_id}/toggle', json={'status': 'completed'}, headers=self.headers)
        self.assertEqual(res_toggle.status_code, 200)

        res_matrix = self.client.get('/api/habits/calendar-matrix', headers=self.headers)
        self.assertEqual(res_matrix.status_code, 200)
