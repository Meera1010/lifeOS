"""
Integration Test Suite for Finance API Blueprint Routes
"""

import unittest
import json
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User


class FinanceRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='route_fin_user', email='route_fin@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

        res = self.client.post('/api/auth/login', json={'email': 'route_fin@example.com', 'password': 'Password123!'})
        self.token = json.loads(res.data)['data']['token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_finance_api_lifecycle(self):
        res_create = self.client.post('/api/finance/transactions', json={
            'type': 'income',
            'amount': 3000.0,
            'description': 'Freelance Client Payment'
        }, headers=self.headers)
        self.assertEqual(res_create.status_code, 201)

        res_summary = self.client.get('/api/finance/summary', headers=self.headers)
        self.assertEqual(res_summary.status_code, 200)
