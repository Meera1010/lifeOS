"""
Unit Test Suite for Auxiliary Services (Tax, Debt, Backup)
"""

import unittest
from backend.services.tax_estimator import TaxEstimator
from backend.services.debt_calculator import DebtPayoffCalculator


class AuxiliaryServicesTestCase(unittest.TestCase):

    def test_tax_estimator(self):
        res = TaxEstimator.calculate_estimated_tax(100000.0, 15000.0, 22.0)
        self.assertEqual(res['taxable_income'], 85000.0)
        self.assertEqual(res['estimated_tax_liability'], 18700.0)

    def test_debt_payoff_calculator(self):
        debts = [
            {'name': 'Credit Card', 'balance': 5000.0, 'interest_rate': 19.99},
            {'name': 'Car Loan', 'balance': 12000.0, 'interest_rate': 4.5}
        ]
        res = DebtPayoffCalculator.calculate_avalanche_payoff(debts, extra_monthly_payment=300.0)
        self.assertEqual(res['strategy'], 'Debt Avalanche')
        self.assertEqual(res['sorted_debts'][0]['name'], 'Credit Card')
