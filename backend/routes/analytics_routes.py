"""
LifeOS Personal Analytics REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.analytics_service import AnalyticsService
from backend.services.life_score_engine import LifeScoreEngine
from backend.services.smart_insights_engine import SmartInsightsEngine
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")

@analytics_bp.route("/dashboard", methods=["GET"])
@require_auth
def get_dashboard_summary():
    data = AnalyticsService.get_dashboard_summary(g.current_user.id)
    return success_response(data=data, message="Dashboard summary analytics retrieved.")

@analytics_bp.route("/reports", methods=["GET"])
@require_auth
def get_analytics_report():
    period = request.args.get("period", "monthly")
    report = AnalyticsService.get_full_analytics_report(g.current_user.id, period=period)
    return success_response(data=report, message="Analytics report retrieved.")

@analytics_bp.route("/life-score", methods=["GET"])
@require_auth
def get_life_score():
    score_data = LifeScoreEngine.calculate_user_life_score(g.current_user.id)
    return success_response(data=score_data, message="Life Score calculated.")

@analytics_bp.route("/insights", methods=["GET"])
@require_auth
def get_insights():
    insights = SmartInsightsEngine.generate_user_insights(g.current_user.id)
    return success_response(data=insights, message="Smart Insights generated.")
