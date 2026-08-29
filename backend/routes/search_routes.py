"""
LifeOS Global Search REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.search_service import SearchService
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response

search_bp = Blueprint("search", __name__, url_prefix="/api/search")

@search_bp.route("", methods=["GET"])
@require_auth
def search_global():
    query = request.args.get("q", "")
    results = SearchService.global_search(g.current_user.id, query)
    return success_response(data=results, message="Global search completed.")
