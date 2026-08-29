"""
LifeOS Journal & Reflection REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.journal_service import JournalService
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response, error_response

journal_bp = Blueprint("journal", __name__, url_prefix="/api/journal")

@journal_bp.route("/entries", methods=["GET"])
@require_auth
def get_entries():
    filters = request.args.to_dict()
    entries = JournalService.get_user_entries(g.current_user.id, filters)
    return success_response(data=entries, message="Journal entries retrieved.")

@journal_bp.route("/entries", methods=["POST"])
@require_auth
def create_entry():
    data = request.get_json() or {}
    ok, result = JournalService.create_entry(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Journal entry created successfully.", status_code=201)

@journal_bp.route("/entries/<int:entry_id>/favorite", methods=["POST"])
@require_auth
def toggle_favorite(entry_id):
    ok, result = JournalService.toggle_favorite(g.current_user.id, entry_id)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Favorite status updated.")

@journal_bp.route("/entries/<int:entry_id>", methods=["DELETE"])
@require_auth
def delete_entry(entry_id):
    ok, msg = JournalService.delete_entry(g.current_user.id, entry_id)
    if not ok:
        return error_response(message=msg, status_code=404)
    return success_response(message=msg)
