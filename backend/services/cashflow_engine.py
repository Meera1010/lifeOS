"""
LifeOS Cash Flow Forecasting & Financial Burn Rate Engine
"""

from datetime import date, timedelta
from typing import Dict, List
from backend.services.finance_service import FinanceService

class CashFlowEngine:

    @staticmethod
    def forecast_cash_flow(user_id: int, months_ahead: int = 6) -> Dict:
        """
        Calculates projected income, expenses, net savings, and runway for N months ahead
        based on historical transaction trends.
        """
        summary = FinanceService.get_monthly_finance_summary(user_id)
        avg_income = summary.get("total_income", 0.0)
        avg_expense = summary.get("total_expenses", 0.0)
        monthly_net = avg_income - avg_expense

        forecast_months = []
        cumulative_savings = summary.get("net_savings", 0.0)
        today = date.today()

        for i in range(1, months_ahead + 1):
            future_date = today + timedelta(days=30 * i)
            cumulative_savings += monthly_net
            forecast_months.append({
                "month_name": future_date.strftime("%b %Y"),
                "projected_income": round(avg_income, 2),
                "projected_expense": round(avg_expense, 2),
                "projected_net": round(monthly_net, 2),
                "cumulative_savings": round(cumulative_savings, 2)
            })

        # Calculate Financial Runway (months of expenses covered by current net savings)
        runway_months = round(cumulative_savings / avg_expense, 1) if avg_expense > 0 else 99.0

        return {
            "forecast_period_months": months_ahead,
            "monthly_burn_rate": round(avg_expense, 2),
            "financial_runway_months": max(0.0, runway_months),
            "monthly_projections": forecast_months
        }
