"""
LifeOS Exhaustive Data Validation & Sanitization Engine
"""

import re
import html

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,30}$")
COLOR_HEX_REGEX = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")

def sanitize_string(input_str: str) -> str:
    """Escapes HTML special characters to prevent XSS attacks."""
    if not input_str or not isinstance(input_str, str):
        return ""
    return html.escape(input_str.strip())

def validate_email(email: str) -> bool:
    """Checks valid email format."""
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))

def validate_username(username: str) -> bool:
    """Checks valid username (3-30 chars, alphanumeric + underscores)."""
    if not username or not isinstance(username, str):
        return False
    return bool(USERNAME_REGEX.match(username.strip()))

def validate_color_hex(hex_str: str) -> bool:
    """Validates hex color string e.g. #4f46e5."""
    if not hex_str or not isinstance(hex_str, str):
        return False
    return bool(COLOR_HEX_REGEX.match(hex_str.strip()))

def validate_numeric_range(val, min_val=None, max_val=None) -> tuple:
    """Validates numeric value bounds."""
    try:
        num = float(val)
    except (ValueError, TypeError):
        return False, "Value must be a valid number."
    
    if min_val is not None and num < min_val:
        return False, f"Value must be at least {min_val}."
    if max_val is not None and num > max_val:
        return False, f"Value must not exceed {max_val}."
    return True, num

def validate_required_fields(data: dict, required_fields: list) -> tuple:
    """Ensures all required keys are present and non-empty in request dictionary."""
    missing = []
    for field in required_fields:
        if field not in data or data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
            missing.append(field)
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, ""
