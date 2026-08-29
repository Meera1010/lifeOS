"""
Unit Test Suite for Finance Service Edge Cases & Budgets
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.models.finance import FinanceCategory
from backend.services.finance_service import FinanceService


class FinanceServiceExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='fin_tester', email='fin_tester@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        
        self.cat = FinanceCategory(user_id=1, name='Dining', type='expense')
        db.session.add(self.cat)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_income_and_expense(self):
        success_inc, res_inc = FinanceService.create_transaction(self.user.id, {
            'type': 'income', 'amount': 5000.0, 'description': 'Monthly Salary'
        })
        self.assertTrue(success_inc)

        success_exp, res_exp = FinanceService.create_transaction(self.user.id, {
            'type': 'expense', 'amount': 1500.0, 'description': 'Apartment Rent'
        })
        self.assertTrue(success_exp)

        summary = FinanceService.get_monthly_finance_summary(self.user.id)
        self.assertEqual(summary['total_income'], 5000.0)
        self.assertEqual(summary['total_expenses'], 1500.0)
        self.assertEqual(summary['net_savings'], 3500.0)
        self.assertEqual(summary['savings_rate'], 70.0)
