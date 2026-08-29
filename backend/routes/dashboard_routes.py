"""
LifeOS Dashboard Overview REST API Routes
"""

from flask import Blueprint, g
from backend.services.analytics_service import AnalyticsService
from backend.services.smart_insights_engine import SmartInsightsEngine
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")

@dashboard_bp.route("/overview", methods=["GET"])
@require_auth
def get_overview():
    summary = AnalyticsService.get_dashboard_summary(g.current_user.id)
    insights = SmartInsightsEngine.generate_user_insights(g.current_user.id)
    summary["smart_insights"] = insights
    return success_response(data=summary, message="Dashboard overview data retrieved.")
