"""
LifeOS Personal Finance Manager Domain Service — Comprehensive Business Logic
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Optional
from sqlalchemy import func, or_, and_, desc, asc
from backend.models.base import db
from backend.models.finance import Transaction, FinanceCategory, Budget, SavingsGoal, RecurringTransaction
from backend.app.constants import TransactionType, FinanceCategoryType
from backend.security.validators import sanitize_string
from backend.utilities.date_utils import parse_date_string, get_month_range, get_week_range


class FinanceService:
    """
    Comprehensive Personal Finance Manager Domain Service providing:
    - Transaction logging (Income, Expense, Transfer) with tags & payment methods
    - Monthly budget tracking with alert thresholds (e.g. alert at 80% limit)
    - Savings Goal progress calculations and target date metrics
    - Recurring transaction schedule generator
    - Financial analytics: Income vs Expense ratios, Savings Rate %, Category Breakdowns
    - Net Worth calculation and cash flow summary metrics
    """

    @staticmethod
    def get_user_transactions(user_id: int, filters: Optional[Dict] = None) -> List[Dict]:
        """Retrieves user financial transactions with category metadata."""
        filters = filters or {}
        query = Transaction.query.filter_by(user_id=user_id, is_deleted=False)

        if filters.get("type"):
            query = query.filter_by(type=filters["type"])
        if filters.get("category_id"):
            try:
                cid = int(filters["category_id"])
                query = query.filter_by(category_id=cid)
            except (ValueError, TypeError):
                pass
        if filters.get("start_date"):
            sd = parse_date_string(filters["start_date"])
            query = query.filter(Transaction.transaction_date >= sd)
        if filters.get("end_date"):
            ed = parse_date_string(filters["end_date"])
            query = query.filter(Transaction.transaction_date <= ed)

        txs = query.order_by(desc(Transaction.transaction_date), desc(Transaction.created_at)).all()
        return [t.to_dict() for t in txs]

    @staticmethod
    def create_transaction(user_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Logs a new income or expense transaction."""
        description = sanitize_string(data.get("description", ""))
        if not description:
            return False, {"error": "Transaction description is required."}

        try:
            amount = float(data.get("amount", 0.0))
        except (ValueError, TypeError):
            return False, {"error": "Invalid transaction amount."}

        if amount <= 0:
            return False, {"error": "Transaction amount must be greater than zero."}

        t_type = data.get("type", TransactionType.EXPENSE.value)
        if t_type not in [t.value for t in TransactionType]:
            t_type = TransactionType.EXPENSE.value

        t_date = parse_date_string(data.get("transaction_date")) if data.get("transaction_date") else date.today()

        category_id = data.get("category_id")
        if category_id:
            cat = FinanceCategory.query.filter_by(id=category_id, user_id=user_id).first()
            if not cat:
                category_id = None

        tx = Transaction(
            user_id=user_id,
            category_id=category_id,
            type=t_type,
            amount=amount,
            description=description,
            transaction_date=t_date,
            payment_method=sanitize_string(data.get("payment_method", "Cash/Card")),
            notes=sanitize_string(data.get("notes", "")),
            tags=sanitize_string(data.get("tags", ""))
        )
        db.session.add(tx)
        db.session.flush()

        # Check Budget Alert if expense
        alert_info = None
        if t_type == TransactionType.EXPENSE.value and category_id:
            alert_info = FinanceService._check_budget_alert(user_id, category_id, t_date)

        db.session.commit()

        return True, {
            "transaction": tx.to_dict(),
            "budget_alert": alert_info
        }

    @staticmethod
    def delete_transaction(user_id: int, tx_id: int) -> Tuple[bool, str]:
        """Soft deletes a transaction."""
        tx = Transaction.query.filter_by(id=tx_id, user_id=user_id, is_deleted=False).first()
        if not tx:
            return False, "Transaction not found."

        tx.soft_delete()
        db.session.commit()
        return True, "Transaction deleted."

    @staticmethod
    def create_budget(user_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Sets monthly category budget limit and alert threshold."""
        category_id = data.get("category_id")
        cat = FinanceCategory.query.filter_by(id=category_id, user_id=user_id).first()
        if not cat:
            return False, {"error": "Invalid finance category."}

        try:
            monthly_limit = float(data.get("monthly_limit", 0.0))
        except (ValueError, TypeError):
            return False, {"error": "Invalid monthly budget limit."}

        if monthly_limit <= 0:
            return False, {"error": "Monthly limit must be greater than zero."}

        today = date.today()
        year = int(data.get("year", today.year))
        month = int(data.get("month", today.month))

        budget = Budget.query.filter_by(
            user_id=user_id,
            category_id=category_id,
            year=year,
            month=month
        ).first()

        if not budget:
            budget = Budget(
                user_id=user_id,
                category_id=category_id,
                monthly_limit=monthly_limit,
                year=year,
                month=month,
                alert_threshold_percentage=float(data.get("alert_threshold_percentage", 80.0))
            )
            db.session.add(budget)
        else:
            budget.monthly_limit = monthly_limit

        db.session.commit()
        return True, budget.to_dict()

    @staticmethod
    def create_savings_goal(user_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Creates a new financial savings goal."""
        title = sanitize_string(data.get("title", ""))
        if not title:
            return False, {"error": "Savings goal title is required."}

        try:
            target = float(data.get("target_amount", 0.0))
            current = float(data.get("current_amount", 0.0))
        except (ValueError, TypeError):
            return False, {"error": "Invalid target or current amount."}

        if target <= 0:
            return False, {"error": "Target amount must be greater than zero."}

        target_date = parse_date_string(data.get("target_date")) if data.get("target_date") else None

        goal = SavingsGoal(
            user_id=user_id,
            title=title,
            target_amount=target,
            current_amount=current,
            target_date=target_date,
            color=data.get("color", "#10b981"),
            icon=data.get("icon", "piggy-bank"),
            notes=sanitize_string(data.get("notes", ""))
        )
        db.session.add(goal)
        db.session.commit()
        return True, goal.to_dict()

    @staticmethod
    def get_monthly_finance_summary(user_id: int, year: Optional[int] = None, month: Optional[int] = None) -> Dict:
        """Calculates total income, total expenses, savings rate, and category breakdowns."""
        today = date.today()
        year = year or today.year
        month = month or today.month

        start_m, end_m = get_month_range(year, month)

        income = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.is_deleted == False,
            Transaction.type == TransactionType.INCOME.value,
            Transaction.transaction_date >= start_m,
            Transaction.transaction_date <= end_m
        ).scalar() or 0.0

        expenses = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.is_deleted == False,
            Transaction.type == TransactionType.EXPENSE.value,
            Transaction.transaction_date >= start_m,
            Transaction.transaction_date <= end_m
        ).scalar() or 0.0

        net_savings = income - expenses
        savings_rate = round((net_savings / income) * 100.0, 1) if income > 0 else 0.0

        # Expense Breakdown by Category
        breakdown = []
        cat_expenses = db.session.query(
            FinanceCategory.id,
            FinanceCategory.name,
            FinanceCategory.color,
            func.sum(Transaction.amount).label("total")
        ).join(Transaction, Transaction.category_id == FinanceCategory.id).filter(
            Transaction.user_id == user_id,
            Transaction.is_deleted == False,
            Transaction.type == TransactionType.EXPENSE.value,
            Transaction.transaction_date >= start_m,
            Transaction.transaction_date <= end_m
        ).group_by(FinanceCategory.id).all()

        for cid, cname, ccolor, ctotal in cat_expenses:
            percentage = round((ctotal / expenses) * 100.0, 1) if expenses > 0 else 0.0
            breakdown.append({
                "category_id": cid,
                "category_name": cname,
                "color": ccolor,
                "total_amount": round(ctotal, 2),
                "percentage": percentage
            })

        return {
            "year": year,
            "month": month,
            "total_income": round(income, 2),
            "total_expenses": round(expenses, 2),
            "net_savings": round(net_savings, 2),
            "savings_rate": savings_rate,
            "category_breakdown": breakdown
        }

    @staticmethod
    def _check_budget_alert(user_id: int, category_id: int, t_date: date) -> Optional[Dict]:
        """Checks if transaction pushes spending over budget alert threshold."""
        budget = Budget.query.filter_by(
            user_id=user_id,
            category_id=category_id,
            year=t_date.year,
            month=t_date.month
        ).first()

        if not budget:
            return None

        start_m, end_m = get_month_range(t_date.year, t_date.month)
        spent = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category_id == category_id,
            Transaction.is_deleted == False,
            Transaction.type == TransactionType.EXPENSE.value,
            Transaction.transaction_date >= start_m,
            Transaction.transaction_date <= end_m
        ).scalar() or 0.0

        percentage = (spent / budget.monthly_limit) * 100.0
        if percentage >= budget.alert_threshold_percentage:
            return {
                "triggered": True,
                "category_name": budget.finance_category.name if budget.finance_category else "Category",
                "limit": budget.monthly_limit,
                "spent": round(spent, 2),
                "percentage": round(percentage, 1)
            }
        return None
