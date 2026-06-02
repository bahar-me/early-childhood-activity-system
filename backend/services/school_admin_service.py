from backend.models import TeacherProfile, ClassProfile, ActivityPlan, School, User
from backend.extensions import db

def get_school_admin_overview(user_id: int):
    user = db.session.get(User, user_id)
    if not user or not user.school_id:
        return {"success": False, "error": "Okul yöneticisi bulunamadı"}

    school = db.session.get(School, user.school_id)
    if not school:
        return {"success": False, "error": "Okul bulunamadı"}

    teachers = db.session.query(TeacherProfile).filter_by(school_id=user.school_id).all()
    classes = db.session.query(ClassProfile).filter_by(school_id=user.school_id).all()
    plans = db.session.query(ActivityPlan).filter_by(school_id=user.school_id).all()

    total_students = sum((c.class_size or 0) for c in classes)

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