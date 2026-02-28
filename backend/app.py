from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from backend.api.auth.routes import auth_bp # Import the auth blueprint
from backend.utils.auth_middleware import token_required
from backend.config import DEBUG


app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route("/")
def home():
    return {"message": "API is running"}

@app.route("/protected")
@token_required
def protected():
    return {"message": "Access granted"}

if __name__ == "__main__":
    app.run(debug=DEBUG)









