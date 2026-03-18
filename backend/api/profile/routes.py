from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.services.profile_service import (
    upsert_teacher_profile,
    get_teacher_profile,
    upsert_class_profile,
    get_class_profile,
)
from backend.utils.auth_middleware import roles_required

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/teacher", methods=["GET"])
@jwt_required()
@roles_required("teacher")
def get_teacher_profile_route():
    user_id = int(get_jwt_identity())
    result = get_teacher_profile(user_id)

    if result["success"]:
        return jsonify(result), 200
    return jsonify({"error": result["error"]}), 404


@profile_bp.route("/teacher", methods=["POST"])
@jwt_required()
@roles_required("teacher")
def upsert_teacher_profile_route():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    result = upsert_teacher_profile(user_id, data)
    if result["success"]:
        return jsonify(result), 200
    return jsonify({"error": result["error"]}), 400


@profile_bp.route("/class", methods=["GET"])
@jwt_required()
@roles_required("teacher")
def get_class_profile_route():
    user_id = int(get_jwt_identity())
    result = get_class_profile(user_id)

    if result["success"]:
        return jsonify(result), 200
    return jsonify({"error": result["error"]}), 404


@profile_bp.route("/class", methods=["POST"])
@jwt_required()
@roles_required("teacher")
def upsert_class_profile_route():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    result = upsert_class_profile(user_id, data)
    if result["success"]:
        return jsonify(result), 200
    return jsonify({"error": result["error"]}), 400