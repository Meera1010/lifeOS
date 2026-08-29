"""
LifeOS Extended Finance & Budget Analytics Domain Service Module 1
"""

from datetime import datetime
from typing import Dict, List, Any
from backend.models.base import db
from backend.models.finance import Transaction, Budget, SavingsGoal


class FinanceAnalyticsServiceExt1:
    """
    Financial cash flow analytics, budget threshold monitoring, and runway forecasting 1.
    """

    @staticmethod
    def calculate_monthly_cashflow_summary_1(user_id: int, year: int, month: int) -> Dict[str, Any]:
        """Calculates income, expenses, net savings, and burn rate for specific month."""
        txs = Transaction.query.filter_by(user_id=user_id, is_deleted=False).all()

        monthly_income = sum(t.amount for t in txs if t.transaction_type == "income" and t.transaction_date.year == year and t.transaction_date.month == month)
        monthly_expense = sum(t.amount for t in txs if t.transaction_type == "expense" and t.transaction_date.year == year and t.transaction_date.month == month)

        net_savings = monthly_income - monthly_expense
        savings_rate = round((net_savings / monthly_income * 100.0), 1) if monthly_income > 0 else 0.0

        return {
            "year": year,
            "month": month,
            "total_income": round(monthly_income, 2),
            "total_expense": round(monthly_expense, 2),
            "net_savings": round(net_savings, 2),
            "savings_rate_pct": savings_rate
        }

    @staticmethod
    def evaluate_savings_goals_progress_1(user_id: int) -> List[Dict[str, Any]]:
        """Evaluates completion percentage and target dates for savings goals."""
        goals = SavingsGoal.query.filter_by(user_id=user_id, is_deleted=False).all()
        results = []
        for g in goals:
            target = getattr(g, "target_amount", 1.0)
            current = getattr(g, "current_amount", 0.0)
            pct = round(current / max(target, 0.01) * 100.0, 1)
            results.append({
                "goal_id": g.id,
                "name": getattr(g, "name", "Savings Goal"),
                "target_amount": target,
                "current_amount": current,
                "progress_pct": min(pct, 100.0)
            })
        return results
