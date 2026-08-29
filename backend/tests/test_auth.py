"""
LifeOS Automated Unit Tests — Authentication & Authorization
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.auth_service import AuthService

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123!",
            "full_name": "Test User"
        }
        ok, res = AuthService.register_user(data)
        self.assertTrue(ok)
        self.assertIn("token", res)
        self.assertEqual(res["user"]["username"], "testuser")

    def test_duplicate_registration_fails(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123!"
        }
        AuthService.register_user(data)
        ok, msg = AuthService.register_user(data)
        self.assertFalse(ok)
        self.assertIn("already taken", msg)

    def test_user_login(self):
        data = {
            "username": "loginuser",
            "email": "login@example.com",
            "password": "Password123!"
        }
        AuthService.register_user(data)
        ok, res = AuthService.login_user({"username": "loginuser", "password": "Password123!"})
        self.assertTrue(ok)
        self.assertIn("token", res)

    def test_invalid_password_login_fails(self):
        data = {
            "username": "loginuser2",
            "email": "login2@example.com",
            "password": "Password123!"
        }
        AuthService.register_user(data)
        ok, msg = AuthService.login_user({"username": "loginuser2", "password": "WrongPassword!"})
        self.assertFalse(ok)
        self.assertIn("Invalid credentials", msg)

if __name__ == "__main__":
    unittest.main()
