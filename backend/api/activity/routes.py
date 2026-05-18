from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from backend.services.activity_service import get_all_activities

activity_bp = Blueprint("activity", __name__)


@activity_bp.route("/", methods=["GET"])
@jwt_required()
def list_activities():
    activities = get_all_activities()
    return jsonify({"activities": activities}), 200