"""
LifeOS Application Entrypoint
"""

import os
from backend.app import create_app
from backend.models.base import db
from data.seed import seed_database_sample_data

env = os.environ.get("FLASK_ENV", "development")
app = create_app(env)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Seed realistic sample data if DB is empty
        seed_database_sample_data()

    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    print(f"============================================================")
    print(f"LifeOS Application running on http://{host}:{port}")
    print(f"============================================================")
    app.run(host=host, port=port, debug=True)
