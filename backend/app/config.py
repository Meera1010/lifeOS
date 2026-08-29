"""
LifeOS Application Configuration Settings
"""

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "lifeos_super_secret_default_key_2026_x998877")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "lifeos_jwt_default_secret_key_2026_y112233")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "uploads")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI", 
        f"sqlite:///{os.path.join(BASE_DIR, 'data', 'lifeos.db')}"
    )

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI",
        f"sqlite:///{os.path.join(BASE_DIR, 'data', 'lifeos_prod.db')}"
    )
    SESSION_COOKIE_SECURE = True

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
