"""
Unit Test Suite for Notification Service
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.notification_service import NotificationService


class NotificationServiceExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='notif_user', email='notif@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_and_read_notification(self):
        notif = NotificationService.create_notification(
            self.user.id,
            'Task Reminder',
            'Your task is due soon!',
            notification_type='task_due'
        )
        self.assertIsNotNone(notif)
        self.assertFalse(notif.is_read)

        success_read, _ = NotificationService.mark_notification_read(self.user.id, notif.id)
        self.assertTrue(success_read)
