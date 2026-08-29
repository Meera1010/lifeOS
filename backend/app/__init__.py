"""
LifeOS Flask Application Factory & Initialization
"""

import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from backend.app.config import config_by_name
from backend.models.base import db

def create_app(config_name="development"):
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend"))
    
    # Load Configuration
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))

    # Initialize Extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register API Blueprints
    from backend.routes.auth_routes import auth_bp
    from backend.routes.user_routes import user_bp
    from backend.routes.task_routes import task_bp
    from backend.routes.habit_routes import habit_bp
    from backend.routes.goal_routes import goal_bp
    from backend.routes.calendar_routes import calendar_bp
    from backend.routes.finance_routes import finance_bp
    from backend.routes.learning_routes import learning_bp
    from backend.routes.focus_routes import focus_bp
    from backend.routes.journal_routes import journal_bp
    from backend.routes.analytics_routes import analytics_bp
    from backend.routes.achievement_routes import achievement_bp
    from backend.routes.notification_routes import notification_bp
    from backend.routes.admin_routes import admin_bp
    from backend.routes.search_routes import search_bp
    from backend.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(habit_bp)
    app.register_blueprint(goal_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(finance_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(focus_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(achievement_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(dashboard_bp)

    # Static Frontend File Server
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        frontend_dir = app.static_folder
        if path.startswith("api/"):
            return jsonify({"success": False, "error": f"API endpoint '/{path}' not found."}), 404
        if path != "" and os.path.exists(os.path.join(frontend_dir, path)):
            return send_from_directory(frontend_dir, path)
        else:
            return send_from_directory(frontend_dir, "index.html")

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"success": False, "error": "Requested resource or endpoint not found."}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"success": False, "error": "Internal server error occurred."}), 500

    return app
