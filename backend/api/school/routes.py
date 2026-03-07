from flask import Blueprint, jsonify, request

from backend.services.auth.school_service import (
    create_school,
    delete_school,
    get_all_schools,
    get_school_by_id,
    update_school
)
from backend.utils.auth_middleware import roles_required

school_bp = Blueprint("school", __name__)

# CREATE SCHOOL
@school_bp.route("/", methods=["POST"])
@roles_required("system_admin")
def create_school_route():
    data = request.get_json() or {}

    result = create_school(
        name=data.get("name"),  
        address=data.get("address")
    )

    if result["success"]:
        return jsonify({
            "message": "School created successfully",
            "school": result["school"]
        }), 201
    
    return jsonify({"error": result["error"]}), 400

@school_bp.route("/", methods=["GET"])
@roles_required("system_admin", "school_admin", "teacher")
def list_schools_route():
    result = get_all_schools()
    return jsonify(result), 200

@school_bp.route("/<int:school_id>", methods=["GET"])
@roles_required("system_admin", "school_admin", "teacher")
def get_school_route(school_id):
    result = get_school_by_id(school_id)

    if result["success"]:
        return jsonify(result), 200
    
    return jsonify({"error": result["error"]}), 404

@school_bp.route("/<int:school_id>", methods=["PUT"])
@roles_required("system_admin", "school_admin") 
def update_school_route(school_id):
    data = request.get_json() or {}

    result = update_school(
        school_id=school_id,
        name=data.get("name"),
        address=data.get("address")
    )

    if result["success"]:
        return jsonify({
            "message": "School updated successfully",
            "school": result["school"]
        }), 200
    
    return jsonify({"error": result["error"]}), 404

@school_bp.route("/<int:school_id>", methods=["DELETE"])
@roles_required("system_admin")
def delete_school_route(school_id):
    result = delete_school(school_id)

    if result["success"]:
        return jsonify({"message": "School deleted successfully"}), 200
    
    return jsonify({"error": result["error"]}), 404
