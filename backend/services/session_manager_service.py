"""
LifeOS Active User Session & JWT Token Revocation Service
"""

from datetime import datetime
from typing import Dict, Any, List
from backend.models.base import db
from backend.models.user import UserSession


class SessionManagerService:
    """
    Manages active user JWT sessions and token revocation lists.
    """

    @staticmethod
    def get_active_user_sessions(user_id: int) -> List[Dict[str, Any]]:
        """Retrieves active sessions for user."""
        sessions = UserSession.query.filter_by(user_id=user_id, is_revoked=False).all()
        return [s.to_dict() for s in sessions]

    @staticmethod
    def revoke_session(user_id: int, session_id: int) -> tuple:
        """Revokes a user session."""
        session = UserSession.query.filter_by(id=session_id, user_id=user_id).first()
        if not session:
            return False, "Session not found."

        session.is_revoked = True
        db.session.commit()
        return True, "Session revoked successfully."
