"""
LifeOS User Management & Profile Service
"""

from backend.models.base import db
from backend.models.user import User, UserProfile
from backend.models.settings import UserSettings, DashboardPreference
from backend.security.validators import sanitize_string, validate_email
from backend.models.audit import AuditLog

class UserService:

    @staticmethod
    def get_user_profile(user_id: int) -> dict:
        user = User.query.get(user_id)
        if not user:
            return None

        profile = user.profile
        if not profile:
            profile = UserProfile(user_id=user.id, full_name=user.username)
            db.session.add(profile)
            db.session.commit()

        data = user.to_dict()
        data["profile"] = profile.to_dict()
        return data

    @staticmethod
    def update_profile(user_id: int, data: dict) -> tuple:
        user = User.query.get(user_id)
        if not user:
            return False, "User not found."

        profile = user.profile
        if not profile:
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)

        if "full_name" in data:
            profile.full_name = sanitize_string(data["full_name"])
        if "bio" in data:
            profile.bio = sanitize_string(data["bio"])
        if "location" in data:
            profile.location = sanitize_string(data["location"])
        if "occupation" in data:
            profile.occupation = sanitize_string(data["occupation"])
        if "website" in data:
            profile.website = sanitize_string(data["website"])
        if "timezone" in data:
            profile.timezone = sanitize_string(data["timezone"])
        if "life_motto" in data:
            profile.life_motto = sanitize_string(data["life_motto"])
        if "avatar_url" in data:
            profile.avatar_url = sanitize_string(data["avatar_url"])

        if "email" in data and data["email"].lower() != user.email:
            new_email = data["email"].lower().strip()
            if not validate_email(new_email):
                return False, "Invalid email address format."
            existing = User.query.filter_by(email=new_email).first()
            if existing and existing.id != user_id:
                return False, "Email address is already in use."
            user.email = new_email

        db.session.commit()
        return True, user.to_dict()

    @staticmethod
    def get_settings(user_id: int) -> dict:
        settings = UserSettings.query.filter_by(user_id=user_id).first()
        if not settings:
            settings = UserSettings(user_id=user_id)
            db.session.add(settings)
            db.session.commit()
        return settings.to_dict()

    @staticmethod
    def update_settings(user_id: int, data: dict) -> tuple:
        settings = UserSettings.query.filter_by(user_id=user_id).first()
        if not settings:
            settings = UserSettings(user_id=user_id)
            db.session.add(settings)

        for key, val in data.items():
            if hasattr(settings, key):
                setattr(settings, key, val)

        db.session.commit()
        return True, settings.to_dict()
