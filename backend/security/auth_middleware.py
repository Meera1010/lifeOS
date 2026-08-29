"""
LifeOS Authentication Middleware & JWT Token Manager
"""

import jwt

from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app, g
from backend.models.user import User, UserSession

def generate_jwt_token(user: User) -> str:
    """Generates a signed JWT token containing user identity and role."""
    payload = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    secret = current_app.config["JWT_SECRET_KEY"]
    return jwt.encode(payload, secret, algorithm="HS256")

def decode_jwt_token(token: str) -> dict:
    """Decodes and validates JWT token."""
    secret = current_app.config["JWT_SECRET_KEY"]
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator requiring a valid JWT Bearer token or Session token in request header."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            # Fallback to custom session header or session cookie
            token = request.headers.get("X-Session-Token") or request.cookies.get("session_token")

        if not token:
            return jsonify({"success": False, "error": "Authentication token missing."}), 401

        payload = decode_jwt_token(token)
        if not payload:
            # Check db session token fallback
            sess = UserSession.query.filter_by(session_token=token, is_active=True).first()
            if sess and not sess.is_expired():
                user = User.query.get(sess.user_id)
            else:
                return jsonify({"success": False, "error": "Invalid or expired authentication token."}), 401
        else:
            user = User.query.get(payload["user_id"])

        if not user or not user.is_active or user.is_deleted:
            return jsonify({"success": False, "error": "User account inactive or disabled."}), 403

        g.current_user = user
        return f(*args, **kwargs)

    return decorated_function

def require_admin(f):
    """Decorator requiring admin privileges."""
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        user = g.current_user
        if not user.is_admin():
            return jsonify({"success": False, "error": "Administrator privilege required."}), 403
        return f(*args, **kwargs)

    return decorated_function
