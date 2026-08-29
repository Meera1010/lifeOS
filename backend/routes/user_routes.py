"""
LifeOS User Profile & Settings REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.user_service import UserService
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response, error_response

user_bp = Blueprint("users", __name__, url_prefix="/api/users")

@user_bp.route("/profile", methods=["GET"])
@require_auth
def get_profile():
    profile = UserService.get_user_profile(g.current_user.id)
    return success_response(data=profile, message="User profile retrieved.")

@user_bp.route("/profile", methods=["PUT"])
@require_auth
def update_profile():
    data = request.get_json() or {}
    ok, result = UserService.update_profile(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Profile updated successfully.")

@user_bp.route("/settings", methods=["GET"])
@require_auth
def get_settings():
    settings = UserService.get_settings(g.current_user.id)
    return success_response(data=settings, message="User settings retrieved.")

@user_bp.route("/settings", methods=["PUT"])
@require_auth
def update_settings():
    data = request.get_json() or {}
    ok, result = UserService.update_settings(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Settings updated successfully.")
