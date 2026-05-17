from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from backend.services.ai_service import generate_recommendation_explanation
from backend.utils.auth_middleware import roles_required

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/explain-recommendations", methods=["POST"])
@jwt_required()
@roles_required("teacher")
def explain_recommendations_route():
    data = request.get_json() or {}

    result = generate_recommendation_explanation(data)

    if result.get("success"):
        return jsonify(result), 200

    return jsonify({"error": result.get("error", "AI explanation failed")}), 400