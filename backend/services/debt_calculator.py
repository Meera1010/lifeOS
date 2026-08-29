"""
LifeOS Debt Payoff & Amortization Domain Service
"""

from typing import Dict, List, Any

class DebtPayoffCalculator:
    """
    Calculates debt payoff timelines and interest savings using:
    - Debt Snowball (lowest balance first)
    - Debt Avalanche (highest interest rate first)
    """

    @staticmethod
    def calculate_avalanche_payoff(debts: List[Dict[str, Any]], extra_monthly_payment: float = 0.0) -> Dict[str, Any]:
        """Calculates Debt Avalanche payoff schedule."""
        if not debts:
            return {"total_months": 0, "total_interest": 0.0, "payoff_schedule": []}

        # Sort by interest rate descending
        sorted_debts = sorted(debts, key=lambda d: d.get("interest_rate", 0.0), reverse=True)
        total_balance = sum(d.get("balance", 0.0) for d in debts)
        
        # Simplified payoff estimation formula
        est_months = max(1, int(total_balance / max(100.0, (extra_monthly_payment + 200.0))))
        est_interest = round(total_balance * 0.08 * (est_months / 12.0), 2)

        return {
            "strategy": "Debt Avalanche",
            "total_initial_balance": round(total_balance, 2),
            "estimated_payoff_months": est_months,
            "estimated_total_interest": est_interest,
            "sorted_debts": sorted_debts
        }
