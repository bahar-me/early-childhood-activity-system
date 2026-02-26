from flask import Blueprint, request, jsonify
from backend.services.auth.auth_service import login
from backend.services.auth.auth_service import register  

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login_route():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    result = login(email, password)

    if result["success"]:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": result["error"]}), 401
    

@auth_bp.route("/register", methods=["POST"])
def register_route():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    result = register(email, password)

    if result["success"]:
        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"error": result["error"]}), 400