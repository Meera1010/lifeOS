"""
LifeOS Achievement System REST API Routes
"""

from flask import Blueprint, g
from backend.services.achievement_engine import AchievementEngine
from backend.security.auth_middleware import require_auth
from backend.utilities.response_utils import success_response

achievement_bp = Blueprint("achievements", __name__, url_prefix="/api/achievements")

@achievement_bp.route("", methods=["GET"])
@require_auth
def get_achievements():
    achievements = AchievementEngine.get_user_achievements(g.current_user.id)
    return success_response(data=achievements, message="Achievements list retrieved.")

@achievement_bp.route("/evaluate", methods=["POST"])
@require_auth
def evaluate_achievements():
    newly_unlocked = AchievementEngine.evaluate_user_achievements(g.current_user.id)
    return success_response(data=newly_unlocked, message="Achievements evaluated.")
