"""
LifeOS Learning Manager REST API Routes
"""

from flask import Blueprint, request, g
from backend.services.learning_service import LearningService
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response, error_response

learning_bp = Blueprint("learning", __name__, url_prefix="/api/learning")

@learning_bp.route("/courses", methods=["GET"])
@require_auth
def get_courses():
    subject_id = int(request.args["subject_id"]) if "subject_id" in request.args else None
    courses = LearningService.get_user_courses(g.current_user.id, subject_id=subject_id)
    return success_response(data=courses, message="Learning courses retrieved.")

@learning_bp.route("/courses", methods=["POST"])
@require_auth
def create_course():
    data = request.get_json() or {}
    ok, result = LearningService.create_course(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Learning course created successfully.", status_code=201)

@learning_bp.route("/study-sessions", methods=["POST"])
@require_auth
def log_study_session():
    data = request.get_json() or {}
    ok, result = LearningService.log_study_session(g.current_user.id, data)
    if not ok:
        return error_response(message=result, status_code=400)
    return success_response(data=result, message="Study session logged successfully.", status_code=201)

@learning_bp.route("/analytics", methods=["GET"])
@require_auth
def get_analytics():
    analytics = LearningService.get_learning_analytics(g.current_user.id)
    return success_response(data=analytics, message="Learning analytics retrieved.")
