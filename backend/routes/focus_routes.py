"""
LifeOS Focus & Pomodoro System REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.focus_service import FocusService
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response, error_response

focus_bp = Blueprint("focus", __name__, url_prefix="/api/focus")

@focus_bp.route("/sessions", methods=["GET"])
@require_auth
def get_sessions():
    days = int(request.args.get("days", 7))
    sessions = FocusService.get_user_focus_sessions(g.current_user.id, days=days)
    return success_response(data=sessions, message="Focus sessions retrieved.")

@focus_bp.route("/sessions", methods=["POST"])
@require_auth
def log_session():
    data = request.get_json() or {}
    ok, result = FocusService.log_focus_session(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Focus session logged successfully.", status_code=201)

@focus_bp.route("/settings", methods=["GET"])
@require_auth
def get_settings():
    settings = FocusService.get_pomodoro_settings(g.current_user.id)
    return success_response(data=settings, message="Pomodoro settings retrieved.")

@focus_bp.route("/settings", methods=["PUT"])
@require_auth
def update_settings():
    data = request.get_json() or {}
    ok, result = FocusService.update_pomodoro_settings(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Pomodoro settings updated.")
