from flask import Blueprint, jsonify, request

from backend.services.auth.auth_service import (
    login, 
    logout,
    refresh_access_token, 
    register
)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register_route():
    data = request.get_json() or {}

    result = register(
        email=data.get("email"),
        password=data.get("password"),
        role=data.get("role", "teacher"),
        school_id=data.get("school_id")
    )

    if result["success"]:
        return jsonify({
            "message": "User registered successfully",
            "user": result["user"]
        }), 201

    return jsonify({"error": result["error"]}), 400

@auth_bp.route("/login", methods=["POST"])
def login_route():
    data = request.get_json() or {}

    result = login(
        email=data.get("email"),
        password=data.get("password")
    )

    if result["success"]:
        return jsonify({
            "message": "Login successful",
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "user": result["user"]
        }), 200

    return jsonify({"error": result["error"]}), 401

@auth_bp.route("/refresh", methods=["POST"])
def refresh_route():
    data = request.get_json() or {}

    result = refresh_access_token(data.get("refresh_token"))
    
    if result["success"]:
        return jsonify({
            "message": "Access token refreshed",
            "access_token": result["access_token"]
        }), 200

    return jsonify({"error": result["error"]}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout_route():
    data = request.get_json() or {}

    result = logout(data.get("refresh_token"))

    if result["success"]:
        return jsonify({"message": "Logged out successfully"}), 200

    return jsonify({"error": result["error"]}), 400
