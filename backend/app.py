from dotenv import load_dotenv
load_dotenv()

from flask import Flask, app
from backend.extensions import db
from backend.api.auth.routes import auth_bp # Import the auth blueprint
from backend.config import DEBUG
import os

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    

    # Configure the app (e.g., database URI, secret key)
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        "sqlite:///" + os.path.join(basedir, "app.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Import models to ensure they are registered with SQLAlchemy
    from backend.models.school import School

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=DEBUG)

    









