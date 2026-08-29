"""
LifeOS Goal Management REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.goal_service import GoalService
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response, error_response

goal_bp = Blueprint("goals", __name__, url_prefix="/api/goals")

@goal_bp.route("", methods=["GET"])
@require_auth
def get_goals():
    filters = request.args.to_dict()
    goals = GoalService.get_user_goals(g.current_user.id, filters)
    return success_response(data=goals, message="Goals retrieved successfully.")

@goal_bp.route("", methods=["POST"])
@require_auth
def create_goal():
    data = request.get_json() or {}
    ok, result = GoalService.create_goal(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Goal created successfully.", status_code=201)

@goal_bp.route("/<int:goal_id>", methods=["PUT"])
@require_auth
def update_goal(goal_id):
    data = request.get_json() or {}
    ok, result = GoalService.update_goal(g.current_user.id, goal_id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Goal updated successfully.")

@goal_bp.route("/milestones/<int:milestone_id>/toggle", methods=["POST"])
@require_auth
def toggle_milestone(milestone_id):
    ok, result = GoalService.toggle_milestone(g.current_user.id, milestone_id)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Milestone toggled successfully.")

@goal_bp.route("/statistics", methods=["GET"])
@require_auth
def get_goal_stats():
    stats = GoalService.get_goal_statistics(g.current_user.id)
    return success_response(data=stats, message="Goal statistics retrieved.")
