import os
from flask import Flask, jsonify
from backend.config import config_by_name
from backend.extensions import db, migrate, jwt

from backend.api.auth.routes import auth_bp # Import the auth blueprint
from backend.api.school.routes import school_bp # Import the school blueprint


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import models to ensure they are registered with SQLAlchemy
    from backend.models import School, User, RefreshToken # noqa: F401

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(school_bp, url_prefix="/api/schools")
    
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


    









