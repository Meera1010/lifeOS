"""
LifeOS Automated Unit Tests — Finance Manager
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.services.auth_service import AuthService
from backend.services.finance_service import FinanceService

class FinanceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        ok, res = AuthService.register_user({
            "username": "finuser",
            "email": "fin@example.com",
            "password": "Password123!"
        })
        self.user_id = res["user"]["id"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_transactions_and_summary(self):
        # Income
        FinanceService.create_transaction(self.user_id, {
            "description": "Salary",
            "type": "income",
            "amount": 5000.0
        })

        # Expense
        FinanceService.create_transaction(self.user_id, {
            "description": "Rent",
            "type": "expense",
            "amount": 1500.0
        })

        summary = FinanceService.get_monthly_finance_summary(self.user_id)
        self.assertEqual(summary["total_income"], 5000.0)
        self.assertEqual(summary["total_expenses"], 1500.0)
        self.assertEqual(summary["net_savings"], 3500.0)
        self.assertEqual(summary["savings_rate"], 70.0)

if __name__ == "__main__":
    unittest.main()
