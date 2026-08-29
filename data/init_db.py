"""
LifeOS Database Initialization CLI Script
"""

import sys
import os

# Ensure backend path is on Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from backend.app import create_app
from backend.models.base import db
from data.seed import seed_database_sample_data

def init_db():
    app = create_app("development")
    with app.app_context():
        print("Dropping and recreating database tables...")
        db.drop_all()
        db.create_all()
        seed_database_sample_data()
        print("Database initialization completed successfully!")

if __name__ == "__main__":
    init_db()
