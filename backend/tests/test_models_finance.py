"""
Unit Test Suite for Finance Models and Budgets
"""

import unittest
from datetime import date
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.models.finance import Transaction, FinanceCategory, Budget, SavingsGoal


class FinanceModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='fin_model_user', email='fin_model@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_savings_goal_progress(self):
        goal = SavingsGoal(user_id=self.user.id, title='New Car', target_amount=10000.0, current_amount=2500.0)
        db.session.add(goal)
        db.session.commit()

        d = goal.to_dict()
        self.assertEqual(d['progress_percentage'], 25.0)
