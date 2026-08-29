"""
LifeOS Personal Finance Manager Models
"""

from datetime import datetime, date
from backend.models.base import db, TimestampMixin, SoftDeleteMixin, SerializerMixin
from backend.app.constants import TransactionType, FinanceCategoryType

class FinanceCategory(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "finance_categories"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(20), default=FinanceCategoryType.EXPENSE.value, nullable=False) # income, expense
    color = db.Column(db.String(20), default="#ef4444", nullable=False)
    icon = db.Column(db.String(50), default="dollar-sign", nullable=False)
    description = db.Column(db.String(255), nullable=True)

    transactions = db.relationship("Transaction", backref="finance_category", lazy="dynamic")
    budgets = db.relationship("Budget", backref="finance_category", lazy="dynamic")


class Transaction(db.Model, TimestampMixin, SoftDeleteMixin, SerializerMixin):
    __tablename__ = "finance_transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("finance_categories.id"), nullable=True, index=True)
    type = db.Column(db.String(20), default=TransactionType.EXPENSE.value, nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    transaction_date = db.Column(db.Date, default=date.today, nullable=False, index=True)
    payment_method = db.Column(db.String(50), default="Credit Card", nullable=False)
    notes = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(255), nullable=True) # CSV of tags

    def to_dict(self, exclude=None, include_relationships=True):
        data = super().to_dict(exclude=exclude)
        if isinstance(self.transaction_date, (date, datetime)):
            data["transaction_date"] = self.transaction_date.strftime("%Y-%m-%d")
        if include_relationships and self.finance_category:
            data["category"] = self.finance_category.to_dict()
        return data


class Budget(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "finance_budgets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("finance_categories.id"), nullable=False)
    monthly_limit = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    alert_threshold_percentage = db.Column(db.Float, default=80.0, nullable=False) # Alert at 80%

    def to_dict(self, exclude=None, include_relationships=True):
        data = super().to_dict(exclude=exclude)
        if include_relationships and self.finance_category:
            data["category"] = self.finance_category.to_dict()
        return data


class SavingsGoal(db.Model, TimestampMixin, SoftDeleteMixin, SerializerMixin):
    __tablename__ = "finance_savings_goals"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0, nullable=False)
    target_date = db.Column(db.Date, nullable=True)
    color = db.Column(db.String(20), default="#10b981", nullable=False)
    icon = db.Column(db.String(50), default="piggy-bank", nullable=False)
    notes = db.Column(db.Text, nullable=True)

    def get_progress_percentage(self):
        if self.target_amount <= 0:
            return 100.0
        return round(min(100.0, (self.current_amount / self.target_amount) * 100.0), 1)

    def to_dict(self, exclude=None):
        data = super().to_dict(exclude=exclude)
        data["progress_percentage"] = self.get_progress_percentage()
        if isinstance(self.target_date, (date, datetime)):
            data["target_date"] = self.target_date.strftime("%Y-%m-%d")
        return data


class RecurringTransaction(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "finance_recurring_transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("finance_categories.id"), nullable=True)
    type = db.Column(db.String(20), default=TransactionType.EXPENSE.value, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.String(20), default="monthly", nullable=False) # daily, weekly, monthly, yearly
    next_due_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
