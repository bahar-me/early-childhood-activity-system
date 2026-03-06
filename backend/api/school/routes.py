from flask import Blueprint, request, jsonify
from backend.extensions import db
from backend.models.school import School
from backend.utils.auth_middleware import roles_required

school_bp = Blueprint("school", __name__)

# CREATE SCHOOL
@school_bp.route("/", methods=["POST"])
@roles_required("system_admin", "school_admin")
def create_school():

    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({"error": "School name is required"}), 400

    new_school = School(
        name=data["name"],
        address=data.get("address")
    )

    db.session.add(new_school)
    db.session.commit()

    return jsonify({
        "id": new_school.id,
        "name": new_school.name,
        "address": new_school.address
    }), 201


# GET ALL SCHOOLS
@school_bp.route("/", methods=["GET"])
@roles_required("system_admin", "school_admin", "teacher")
def get_schools():
    schools = School.query.all()

    result = []
    for school in schools:
        result.append({
            "id": school.id,
            "name": school.name,
            "address": school.address
        })

    return jsonify(result), 200