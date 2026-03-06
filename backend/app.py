from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_migrate import Migrate
from backend.extensions import db
from backend.api.auth.routes import auth_bp # Import the auth blueprint
from backend.config import DEBUG
import os

basedir = os.path.abspath(os.path.dirname(__file__))

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    

    # Configure the app (e.g., database URI, secret key)
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        "sqlite:///" + os.path.join(basedir, "app.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    print("DB PATH:", app.config["SQLALCHEMY_DATABASE_URI"])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to ensure they are registered with SQLAlchemy
    from backend.models.school import School
    from backend.models.user import User

    # Import blueprints
    from backend.api.school.routes import school_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(school_bp, url_prefix="/api/schools")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=DEBUG)

    









