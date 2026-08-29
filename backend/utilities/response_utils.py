"""
LifeOS Standardized REST API Response Formatter
"""

from flask import jsonify

def success_response(data=None, message="Success", status_code=200, meta=None):
    """Formats standard JSON success response."""
    payload = {
        "success": True,
        "message": message,
        "data": data if data is not None else {}
    }
    if meta:
        payload["meta"] = meta
    return jsonify(payload), status_code

def error_response(message="An error occurred", status_code=400, errors=None):
    """Formats standard JSON error response."""
    payload = {
        "success": False,
        "error": message
    }
    if errors:
        payload["details"] = errors
    return jsonify(payload), status_code

def paginated_response(items, page, per_page, total_items, message="Items retrieved successfully"):
    """Formats standard JSON paginated collection response."""
    total_pages = (total_items + per_page - 1) // per_page if per_page > 0 else 1
    meta = {
        "page": page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }
    return success_response(data=items, message=message, status_code=200, meta=meta)
