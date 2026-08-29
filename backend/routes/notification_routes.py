"""
LifeOS Notification System REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.notification_service import NotificationService
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response, error_response

notification_bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")

@notification_bp.route("", methods=["GET"])
@require_auth
def get_notifications():
    unread = request.args.get("unread_only", "false").lower() == "true"
    limit = int(request.args.get("limit", 50))
    notifs = NotificationService.get_user_notifications(g.current_user.id, unread_only=unread, limit=limit)
    unread_count = NotificationService.get_unread_count(g.current_user.id)
    return success_response(
        data={"notifications": notifs, "unread_count": unread_count},
        message="Notifications retrieved."
    )

@notification_bp.route("/<int:notification_id>/read", methods=["PUT"])
@require_auth
def mark_read(notification_id):
    ok, result = NotificationService.mark_notification_read(g.current_user.id, notification_id)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Notification marked as read.")

@notification_bp.route("/mark-all-read", methods=["PUT"])
@require_auth
def mark_all_read():
    ok, msg = NotificationService.mark_all_read(g.current_user.id)
    return success_response(message=msg)
