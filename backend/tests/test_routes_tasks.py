"""
Integration Test Suite for Tasks API Blueprint Routes
"""

import unittest
import json
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User


class TasksRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='route_task_user', email='route_task@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

        # Login to get JWT Token
        res = self.client.post('/api/auth/login', json={'email': 'route_task@example.com', 'password': 'Password123!'})
        self.token = json.loads(res.data)['data']['token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_tasks_api_lifecycle(self):
        # Create Task
        res_create = self.client.post('/api/tasks', json={'title': 'API Route Task', 'priority': 'high'}, headers=self.headers)
        self.assertEqual(res_create.status_code, 201)
        data_c = json.loads(res_create.data)['data']
        task_id = data_c['id']

        # Get Tasks
        res_get = self.client.get('/api/tasks', headers=self.headers)
        self.assertEqual(res_get.status_code, 200)

        # Update Task
        res_put = self.client.put(f'/api/tasks/{task_id}', json={'status': 'completed'}, headers=self.headers)
        self.assertEqual(res_put.status_code, 200)

        # Delete Task
        res_del = self.client.delete(f'/api/tasks/{task_id}', headers=self.headers)
        self.assertEqual(res_del.status_code, 200)
