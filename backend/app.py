from dotenv import load_dotenv

from backend.models import user
load_dotenv()

from flask import Flask, jsonify, request
from backend.api.auth.routes import auth_bp # Import the auth blueprint
from backend.utils.auth_middleware import token_required, roles_required
from backend.config import DEBUG


app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route("/")
def home():
    return {"message": "API is running"}

@app.route("/api/protected", methods=["GET"])
@token_required
def protected_route():
    return jsonify({
        "message": "You are authenticated.", 
        "user": request.user
        })

@app.route("/api/teacher-only", methods=["GET"])
@token_required
@roles_required("teacher")
def teacher_only():
    return jsonify({"message": "Welcome teacher."})

@app.route("/api/school-admin-only", methods=["GET"])
@token_required
@roles_required("school_admin")
def school_admin_only():
    return jsonify({"message": "Welcome school admin."})

@app.route("/api/system-admin-only", methods=["GET"])
@token_required 
@roles_required("system_admin")
def system_admin_only():
    return jsonify({"message": "Welcome system admin."})


if __name__ == "__main__":
    app.run(debug=DEBUG)









