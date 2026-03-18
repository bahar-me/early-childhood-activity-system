from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.services.activity_plan_service import create_activity_plan
from backend.utils.auth_middleware import roles_required

activity_plan_bp = Blueprint("activity_plan", __name__)


@activity_plan_bp.route("/", methods=["POST"])
@jwt_required()
@roles_required("teacher")
def create_activity_plan_route():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    result = create_activity_plan(user_id, data)
    if result["success"]:
        return jsonify(result), 201
    return jsonify({"error": result["error"]}), 400