"""
LifeOS Administrator Panel REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.admin_service import AdminService
from backend.security.auth_middleware import require_admin
from backend.utilities.response_utils import success_response, error_response, paginated_response

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.route("/users", methods=["GET"])
@require_admin
def list_users():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    search = request.args.get("search")
    users, total = AdminService.list_all_users(page=page, per_page=per_page, search_term=search)
    return paginated_response(items=users, page=page, per_page=per_page, total_items=total, message="User accounts retrieved.")

@admin_bp.route("/users", methods=["POST"])
@require_admin
def create_user():
    data = request.get_json() or {}
    ok, result = AdminService.create_user_by_admin(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="User account created by admin.", status_code=201)

@admin_bp.route("/users/<int:target_user_id>/status", methods=["PUT"])
@require_admin
def toggle_status(target_user_id):
    ok, result = AdminService.toggle_user_active_status(g.current_user.id, target_user_id)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="User active status updated.")

@admin_bp.route("/users/<int:target_user_id>", methods=["DELETE"])
@require_admin
def delete_user(target_user_id):
    ok, msg = AdminService.delete_user_by_admin(g.current_user.id, target_user_id)
    if not ok:
        return error_response(message=msg, status_code=400)
    return success_response(message=msg)

@admin_bp.route("/audit-logs", methods=["GET"])
@require_admin
def get_audit_logs():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    logs, total = AdminService.get_system_audit_logs(page=page, per_page=per_page)
    return paginated_response(items=logs, page=page, per_page=per_page, total_items=total, message="Audit logs retrieved.")

@admin_bp.route("/statistics", methods=["GET"])
@require_admin
def get_system_stats():
    stats = AdminService.get_system_statistics()
    return success_response(data=stats, message="System administration statistics retrieved.")
