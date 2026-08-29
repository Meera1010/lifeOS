"""
LifeOS Authentication REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.auth_service import AuthService
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response, error_response

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    ok, result = AuthService.register_user(data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="User registered successfully.", status_code=201)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    ip = request.remote_addr
    ua = request.headers.get("User-Agent")
    ok, result = AuthService.login_user(data, ip_address=ip, user_agent=ua)
    if not ok:
        return error_response(message=result, status_code=401)
    return success_response(data=result, message="Authentication successful.", status_code=200)

@auth_bp.route("/me", methods=["GET"])
@require_auth
def get_current_user():
    return success_response(data=g.current_user.to_dict(), message="Current user profile retrieved.")

@auth_bp.route("/change-password", methods=["POST"])
@require_auth
def change_password():
    data = request.get_json() or {}
    old_pwd = data.get("old_password")
    new_pwd = data.get("new_password")
    ok, msg = AuthService.change_password(g.current_user.id, old_pwd, new_pwd)
    if not ok:
        return error_response(message=msg, status_code=400)
    return success_response(message=msg)
