"""
LifeOS User Profile Management Domain Service
"""

from typing import Dict, Any, Optional
from backend.models.base import db
from backend.models.user import User, UserProfile
from backend.security.validators import sanitize_string, validate_email


class UserProfileService:
    """
    Manages user profile bio, occupation, location, life motto, and preferences.
    """

    @staticmethod
    def get_profile_by_user_id(user_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves user profile data."""
        user = User.query.get(user_id)
        if not user:
            return None
        return user.to_dict()

    @staticmethod
    def update_profile(user_id: int, data: Dict[str, Any]) -> tuple:
        """Updates user profile attributes."""
        user = User.query.get(user_id)
        if not user:
            return False, "User not found."

        if "email" in data and data["email"] != user.email:
            new_email = sanitize_string(data["email"]).lower()
            if not validate_email(new_email):
                return False, "Invalid email address."
            if User.query.filter_by(email=new_email).first():
                return False, "Email already in use."
            user.email = new_email

        profile = user.profile
        if not profile:
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)

        if "full_name" in data:
            profile.full_name = sanitize_string(data["full_name"])
        if "bio" in data:
            profile.bio = sanitize_string(data["bio"])
        if "occupation" in data:
            profile.occupation = sanitize_string(data["occupation"])
        if "location" in data:
            profile.location = sanitize_string(data["location"])
        if "life_motto" in data:
            profile.life_motto = sanitize_string(data["life_motto"])

        db.session.commit()
        return True, user.to_dict()
