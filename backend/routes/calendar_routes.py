"""
LifeOS Calendar REST API Routes
"""

from datetime import datetime, date
from flask import Blueprint, request, g
from backend.services.calendar_service import CalendarService
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response, error_response
from backend.utilities.date_utils import parse_datetime_string

calendar_bp = Blueprint("calendar", __name__, url_prefix="/api/calendar")

@calendar_bp.route("/events", methods=["GET"])
@require_auth
def get_events():
    start_str = request.args.get("start")
    end_str = request.args.get("end")
    start_dt = parse_datetime_string(start_str) if start_str else datetime.utcnow() - timedelta(days=15)
    end_dt = parse_datetime_string(end_str) if end_str else datetime.utcnow() + timedelta(days=15)

    events = CalendarService.get_events_for_range(g.current_user.id, start_dt, end_dt)
    return success_response(data=events, message="Calendar events retrieved successfully.")

@calendar_bp.route("/events", methods=["POST"])
@require_auth
def create_event():
    data = request.get_json() or {}
    ok, result = CalendarService.create_event(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Calendar event created successfully.", status_code=201)

@calendar_bp.route("/events/<int:event_id>", methods=["PUT"])
@require_auth
def update_event(event_id):
    data = request.get_json() or {}
    ok, result = CalendarService.update_event(g.current_user.id, event_id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Calendar event updated successfully.")

@calendar_bp.route("/events/<int:event_id>", methods=["DELETE"])
@require_auth
def delete_event(event_id):
    ok, msg = CalendarService.delete_event(g.current_user.id, event_id)
    if not ok:
        return error_response(message=msg, status_code=404)
    return success_response(message=msg)

@calendar_bp.route("/month-view", methods=["GET"])
@require_auth
def get_month_view():
    year = int(request.args.get("year", date.today().year))
    month = int(request.args.get("month", date.today().month))
    view_data = CalendarService.get_month_view(g.current_user.id, year, month)
    return success_response(data=view_data, message="Month calendar view retrieved.")
