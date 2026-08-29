"""
LifeOS Habit Tracker REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.habit_service import HabitService
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response, error_response

habit_bp = Blueprint("habits", __name__, url_prefix="/api/habits")

@habit_bp.route("", methods=["GET"])
@require_auth
def get_habits():
    inc_arch = request.args.get("include_archived", "false").lower() == "true"
    habits = HabitService.get_user_habits(g.current_user.id, include_archived=inc_arch)
    return success_response(data=habits, message="Habits retrieved successfully.")

@habit_bp.route("", methods=["POST"])
@require_auth
def create_habit():
    data = request.get_json() or {}
    ok, result = HabitService.create_habit(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Habit created successfully.", status_code=201)

@habit_bp.route("/<int:habit_id>/toggle", methods=["POST"])
@require_auth
def toggle_habit(habit_id):
    data = request.get_json() or {}
    target_date = data.get("completion_date")
    status = data.get("status", "completed")
    ok, result = HabitService.toggle_habit_completion(g.current_user.id, habit_id, target_date_str=target_date, status=status)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Habit completion toggled successfully.")

@habit_bp.route("/calendar-matrix", methods=["GET"])
@require_auth
def get_calendar_matrix():
    days = int(request.args.get("days", 30))
    matrix = HabitService.get_habit_calendar_data(g.current_user.id, days=days)
    return success_response(data=matrix, message="Habit completion matrix retrieved.")

@habit_bp.route("/statistics", methods=["GET"])
@require_auth
def get_habit_stats():
    stats = HabitService.get_habit_statistics(g.current_user.id)
    return success_response(data=stats, message="Habit statistics retrieved.")
