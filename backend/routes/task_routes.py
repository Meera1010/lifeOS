"""
LifeOS Task Manager REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.task_service import TaskService
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response, error_response

task_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")

@task_bp.route("", methods=["GET"])
@require_auth
def get_tasks():
    filters = request.args.to_dict()
    tasks = TaskService.get_user_tasks(g.current_user.id, filters)
    return success_response(data=tasks, message="Tasks retrieved successfully.")

@task_bp.route("", methods=["POST"])
@require_auth
def create_task():
    data = request.get_json() or {}
    ok, result = TaskService.create_task(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Task created successfully.", status_code=201)

@task_bp.route("/<int:task_id>", methods=["PUT"])
@require_auth
def update_task(task_id):
    data = request.get_json() or {}
    ok, result = TaskService.update_task(g.current_user.id, task_id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Task updated successfully.")

@task_bp.route("/<int:task_id>", methods=["DELETE"])
@require_auth
def delete_task(task_id):
    ok, msg = TaskService.delete_task(g.current_user.id, task_id)
    if not ok:
        return error_response(message=msg, status_code=404)
    return success_response(message=msg)

@task_bp.route("/subtasks/<int:subtask_id>/toggle", methods=["POST"])
@require_auth
def toggle_subtask(subtask_id):
    ok, result = TaskService.toggle_subtask(g.current_user.id, subtask_id)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Subtask toggled successfully.")

@task_bp.route("/statistics", methods=["GET"])
@require_auth
def get_task_stats():
    stats = TaskService.get_task_statistics(g.current_user.id)
    return success_response(data=stats, message="Task statistics retrieved.")
