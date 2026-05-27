from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from backend.services.activity_service import get_all_activities, create_activity, update_activity

activity_bp = Blueprint("activity", __name__)


@activity_bp.route("/", methods=["GET"])
@jwt_required()
def list_activities():
    activities = get_all_activities()
    return jsonify({"activities": activities}), 200

@activity_bp.route("/", methods=["POST"])
@jwt_required()
def create_activity_route():
    data = request.get_json() or {}

    try:
        activity = create_activity(data)
        return jsonify({"activity": activity}), 201
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        return jsonify({"error": "Bilinmeyen bir hata oluştu"}), 500
    
@activity_bp.route("/<int:activity_id>", methods=["PUT"])
@jwt_required()
def update_activity_route(activity_id: int):
    data = request.get_json() or {}

    try:
        activity = update_activity(activity_id, data)
        return jsonify({"activity": activity}), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        return jsonify({"error": "Bilinmeyen bir hata oluştu"}), 500