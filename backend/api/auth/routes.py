from flask import Blueprint, request, jsonify
from backend.services.auth.auth_service import login, register, refresh_access_token, logout  

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login_route():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    
    email = data.get("email")
    password = data.get("password")

    result = login(email, password)

    if result["success"]:
        return jsonify({"access_token": result["access_token"], "refresh_token": result["refresh_token"]}), 200
    else:
        return jsonify({"error": result["error"]}), 401
    

@auth_bp.route("/register", methods=["POST"])
def register_route():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    
    email = data.get("email")
    password = data.get("password")

    result = register(email, password)

    if result["success"]:
        return jsonify({"message": "User registered successfully"}), 201
    
    return jsonify({"error": result["error"]}), 400

@auth_bp.route("/refresh", methods=["POST"])
def refresh_route():
    data = request.get_json()
    refresh_token = data.get("refresh_token")

    result = refresh_access_token(refresh_token)

    if result["success"]:
        return jsonify({"access_token": result["access_token"]}), 200
    else:
        return jsonify({"error": result["error"]}), 401
    
@auth_bp.route("/logout", methods=["POST"])
def logout_route():
    data = request.get_json()
    refresh_token = data.get("refresh_token")

    result = logout(refresh_token)

    if result["success"]:
        return jsonify({"message": "Logged out successfully"}), 200
    else:
        return jsonify({"error": result["error"]}), 400

   