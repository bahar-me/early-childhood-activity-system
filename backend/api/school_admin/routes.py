from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.services.school_admin_service import get_school_admin_overview
from backend.utils.auth_middleware import roles_required

school_admin_bp = Blueprint("school_admin", __name__)


@school_admin_bp.route("/overview", methods=["GET"])
@jwt_required()
@roles_required("school_admin")
def school_admin_overview_route():
    user_id = int(get_jwt_identity())
    result = get_school_admin_overview(user_id)

    if result["success"]:
        return jsonify(result), 200
    return jsonify({"error": result["error"]}), 400