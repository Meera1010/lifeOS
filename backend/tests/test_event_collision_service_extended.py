"""
Unit Test Suite for Calendar Event Collision & Conflict Resolution Service
"""

import unittest
from datetime import datetime, timedelta
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.event_collision_service import EventCollisionService


class EventCollisionServiceExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='collision_user', email='collision@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_conflict_detection_and_free_slot(self):
        start = (datetime.utcnow() + timedelta(hours=1)).isoformat()
        end = (datetime.utcnow() + timedelta(hours=2)).isoformat()

        res = EventCollisionService.detect_event_conflicts(self.user.id, start, end)
        self.assertFalse(res['has_conflict'])

        slot_res = EventCollisionService.suggest_next_free_slot(self.user.id, duration_minutes=60)
        self.assertIn('suggested_slot', slot_res)
