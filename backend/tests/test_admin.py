"""
LifeOS Automated Unit Tests — Admin Panel & RBAC
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.services.auth_service import AuthService
from backend.services.admin_service import AdminService

class AdminTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        ok, admin_res = AuthService.register_user({
            "username": "adminuser",
            "email": "admin@example.com",
            "password": "Password123!",
            "role": "admin"
        })
        self.admin_id = admin_res["user"]["id"]

        ok, user_res = AuthService.register_user({
            "username": "normaluser",
            "email": "normal@example.com",
            "password": "Password123!"
        })
        self.user_id = user_res["user"]["id"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_admin_list_and_toggle_user(self):
        users, total = AdminService.list_all_users()
        self.assertEqual(total, 2)

        ok, toggled = AdminService.toggle_user_active_status(self.admin_id, self.user_id)
        self.assertTrue(ok)
        self.assertFalse(toggled["is_active"])

if __name__ == "__main__":
    unittest.main()
