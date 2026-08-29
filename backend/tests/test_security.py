"""
LifeOS Automated Unit Tests — Security & Input Validation
"""

import unittest
from backend.security.password_hasher import hash_password, verify_password, validate_password_strength
from backend.security.validators import sanitize_string, validate_email, validate_username

class SecurityTestCase(unittest.TestCase):

    def test_password_hashing(self):
        pwd = "ComplexPassword123!"
        hashed = hash_password(pwd)
        self.assertTrue(verify_password(hashed, pwd))
        self.assertFalse(verify_password(hashed, "WrongPass"))

    def test_password_strength_validation(self):
        is_valid, msg = validate_password_strength("weak")
        self.assertFalse(is_valid)

        is_valid, msg = validate_password_strength("StrongPass123!")
        self.assertTrue(is_valid)

    def test_input_sanitization(self):
        dirty = "<script>alert('xss')</script>"
        clean = sanitize_string(dirty)
        self.assertNotIn("<script>", clean)
        self.assertIn("&lt;script&gt;", clean)

if __name__ == "__main__":
    unittest.main()
