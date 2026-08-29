"""
Unit Test Suite for Cash Flow Forecasting Engine
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.cashflow_engine import CashFlowEngine


class CashFlowEngineExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='cashflow_user', email='cashflow@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_cash_flow_forecast(self):
        res = CashFlowEngine.forecast_cash_flow(self.user.id, months_ahead=6)
        self.assertEqual(res['forecast_period_months'], 6)
        self.assertEqual(len(res['monthly_projections']), 6)
