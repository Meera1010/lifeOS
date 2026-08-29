"""
LifeOS Password Security & Validation Utilities
"""

import re
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    """Hashes a raw password using secure PBKDF2:SHA256."""
    return generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

def verify_password(password_hash: str, password: str) -> bool:
    """Verifies a plain password against the stored hash."""
    if not password_hash or not password:
        return False
    return check_password_hash(password_hash, password)

def validate_password_strength(password: str) -> tuple:
    """
    Validates password complexity:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        return False, "Password must contain at least one special character."
    return True, "Password meets security requirements."
