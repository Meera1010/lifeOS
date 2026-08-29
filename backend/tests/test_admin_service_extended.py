"""
Unit Test Suite for Administrator Service & RBAC
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.admin_service import AdminService


class AdminServiceExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.admin = User(username='admin_user', email='admin@example.com', role='admin')
        self.admin.set_password('AdminPass123!')
        
        self.user = User(username='normal_user', email='normal@example.com', role='user')
        self.user.set_password('UserPass123!')

        db.session.add(self.admin)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_all_users(self):
        users, total = AdminService.list_all_users()
        self.assertGreaterEqual(len(users), 2)

    def test_toggle_user_status(self):
        success, res = AdminService.toggle_user_active_status(self.admin.id, self.user.id)
        self.assertTrue(success)
        self.assertFalse(res['is_active'])
