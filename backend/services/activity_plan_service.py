import json
from typing import Any, Dict

from backend.extensions import db
from backend.models import ActivityPlan, TeacherProfile, ClassProfile


def create_activity_plan(user_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
    teacher = TeacherProfile.query.filter_by(user_id=user_id).first()
    if not teacher:
        return {"success": False, "error": "Teacher profile not found"}

    class_profile = ClassProfile.query.filter_by(teacher_id=teacher.id).first()
    if not class_profile:
        return {"success": False, "error": "Class profile not found"}

    activity_ids = payload.get("activity_ids", [])
    notes = payload.get("notes", "")

    if not activity_ids:
        return {"success": False, "error": "At least one activity is required"}

    plan = ActivityPlan(
        teacher_id=teacher.id,
        class_id=class_profile.id,
        school_id=teacher.school_id,
        activity_ids=json.dumps(activity_ids),
        notes=notes,
    )

    db.session.add(plan)
    db.session.commit()

    return {"success": True, "plan": plan.to_dict()}