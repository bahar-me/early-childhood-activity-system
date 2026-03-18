from backend.models import TeacherProfile, ClassProfile, ActivityPlan, School, User


def get_school_admin_overview(user_id: int):
    user = User.query.get(user_id)
    if not user or not user.school_id:
        return {"success": False, "error": "School admin not linked to a school"}

    school = School.query.get(user.school_id)
    if not school:
        return {"success": False, "error": "School not found"}

    teachers = TeacherProfile.query.filter_by(school_id=user.school_id).all()
    classes = ClassProfile.query.filter_by(school_id=user.school_id).all()
    plans = ActivityPlan.query.filter_by(school_id=user.school_id).all()

    total_students = sum(c.class_size for c in classes)

    return {
        "success": True,
        "school": school.to_dict(),
        "stats": {
            "teachers": len(teachers),
            "classes": len(classes),
            "students": total_students,
            "activity_plans": len(plans),
        },
        "teachers_list": [t.to_dict() for t in teachers],
        "classes_list": [c.to_dict() for c in classes],
        "plans_list": [p.to_dict() for p in plans],
    }