from typing import Any, Dict, Optional

from backend.extensions import db
from backend.models import School


def create_school(name: str, address: Optional[str] = None) -> Dict[str, Any]:
    if not name:
        return {"success": False, "error": "School name is required"}

    school = School(name=name, address=address)
    db.session.add(school)
    db.session.commit()

    return {"success": True, "school": school.to_dict()}

def get_all_schools() -> Dict[str, Any]:
    schools = School.query.order_by(School.id.asc()).all()
    return {
        "success": True, 
        "schools": [school.to_dict() for school in schools]
    }

def get_school_by_id(school_id: int) -> Dict[str, Any]:
    school = db.session.get(School, school_id)
    if not school:
        return {"success": False, "error": "School not found"}
    
    return {"success": True, "school": school.to_dict()}

def update_school(school_id: int, name: Optional[str], address: Optional[str] = None) -> Dict[str, Any]:
    school = db.session.get(School, school_id)
    if not school:
        return {"success": False, "error": "School not found"}

    if name is not None and name.strip():
        school.name = name.strip()

    if address is not None:
        school.address = address.strip() if isinstance(address, str) else address

    db.session.commit()
    db.session.refresh(school)

    return {"success": True, "school": school.to_dict()}

def delete_school(school_id: int) -> Dict[str, Any]:
    school = db.session.get(School, school_id)
    if not school:
        return {"success": False, "error": "School not found"}

    db.session.delete(school)
    db.session.commit()

    return {"success": True, "message": "School deleted successfully"}