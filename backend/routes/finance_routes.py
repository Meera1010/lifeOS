"""
LifeOS Finance Manager REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.finance_service import FinanceService
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response, error_response

finance_bp = Blueprint("finance", __name__, url_prefix="/api/finance")

@finance_bp.route("/transactions", methods=["GET"])
@require_auth
def get_transactions():
    filters = request.args.to_dict()
    txs = FinanceService.get_user_transactions(g.current_user.id, filters)
    return success_response(data=txs, message="Financial transactions retrieved.")

@finance_bp.route("/transactions", methods=["POST"])
@require_auth
def create_transaction():
    data = request.get_json() or {}
    ok, result = FinanceService.create_transaction(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Transaction logged successfully.", status_code=201)

@finance_bp.route("/summary", methods=["GET"])
@require_auth
def get_summary():
    year = int(request.args["year"]) if "year" in request.args else None
    month = int(request.args["month"]) if "month" in request.args else None
    summary = FinanceService.get_monthly_finance_summary(g.current_user.id, year=year, month=month)
    return success_response(data=summary, message="Monthly financial summary retrieved.")

@finance_bp.route("/savings-goals", methods=["POST"])
@require_auth
def create_savings_goal():
    data = request.get_json() or {}
    ok, result = FinanceService.create_savings_goal(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Savings goal created successfully.", status_code=201)
