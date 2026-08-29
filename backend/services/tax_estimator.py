"""
LifeOS Income Tax & Deduction Estimation Domain Service
"""

from typing import Dict, Any

class TaxEstimator:
    """
    Calculates estimated federal income tax and net take-home pay
    based on income transactions and deductible expense categories.
    """

    @staticmethod
    def calculate_estimated_tax(gross_income: float, deductible_expenses: float, tax_rate_percentage: float = 22.0) -> Dict[str, Any]:
        """Calculates taxable income and tax liability."""
        gross = max(0.0, float(gross_income))
        deductions = max(0.0, float(deductible_expenses))
        taxable_income = max(0.0, gross - deductions)
        
        rate = max(0.0, min(100.0, float(tax_rate_percentage))) / 100.0
        estimated_tax = round(taxable_income * rate, 2)
        net_after_tax = round(gross - estimated_tax, 2)

        return {
            "gross_income": round(gross, 2),
            "deductible_expenses": round(deductions, 2),
            "taxable_income": round(taxable_income, 2),
            "effective_tax_rate": tax_rate_percentage,
            "estimated_tax_liability": estimated_tax,
            "net_after_tax_income": net_after_tax
        }
