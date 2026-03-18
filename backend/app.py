import os
from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import config_by_name
from backend.extensions import db, migrate, jwt

from backend.api.auth.routes import auth_bp # Import the auth blueprint
from backend.api.school.routes import school_bp # Import the school blueprint
from backend.api.profile.routes import profile_bp # Import the profile blueprint
from backend.api.activity_plan.routes import activity_plan_bp # Import the activity plan blueprint
from backend.api.school_admin.routes import school_admin_bp # Import the school admin blueprint

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import models to ensure they are registered with SQLAlchemy
    from backend.models import School, User, RefreshToken # noqa: F401

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(school_bp, url_prefix="/api/schools")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(activity_plan_bp, url_prefix="/api/activity-plans")
    app.register_blueprint(school_admin_bp, url_prefix="/api/school-admin")


    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "message": "Backend is running"}), 200

    @app.errorhandler(404)
    def not_found(_e):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(_e):
        return jsonify({"error": "Internal server error"}), 500
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run()


    









