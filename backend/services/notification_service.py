"""
LifeOS Notification System Domain Service
"""

from datetime import datetime
from backend.models.base import db
from backend.models.notification import Notification, NotificationPreference

class NotificationService:

    @staticmethod
    def get_user_notifications(user_id: int, unread_only: bool = False, limit: int = 50) -> list:
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        notifs = query.order_by(Notification.created_at.desc()).limit(limit).all()
        return [n.to_dict() for n in notifs]

    @staticmethod
    def get_unread_count(user_id: int) -> int:
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()

    @staticmethod
    def mark_notification_read(user_id: int, notification_id: int) -> tuple:
        notif = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if not notif:
            return False, "Notification not found."

        notif.mark_as_read()
        db.session.commit()
        return True, notif.to_dict()

    @staticmethod
    def mark_all_read(user_id: int) -> tuple:
        Notification.query.filter_by(user_id=user_id, is_read=False).update(
            {"is_read": True, "read_at": datetime.utcnow()}
        )
        db.session.commit()
        return True, "All notifications marked as read."

    @staticmethod
    def create_notification(user_id: int, title: str, message: str, notification_type: str = "system_alert", severity: str = "info", entity_type: str = None, entity_id: int = None) -> Notification:
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            severity=severity,
            entity_type=entity_type,
            entity_id=entity_id
        )
        db.session.add(notif)
        db.session.commit()
        return notif
