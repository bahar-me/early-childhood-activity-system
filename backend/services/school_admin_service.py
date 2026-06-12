from backend.models import TeacherProfile, ClassProfile, ActivityPlan, School, User
from backend.extensions import db

def get_school_admin_overview(user_id: int):
    user = db.session.get(User, user_id)
    if not user or not user.school_id:
        return {"success": False, "error": "Okul yöneticisi bulunamadı"}

    school = db.session.get(School, user.school_id)
    if not school:
        return {"success": False, "error": "Okul bulunamadı"}

    plans = (
        db.session.query(ActivityPlan)
        .filter_by(school_id=user.school_id)
        .order_by(ActivityPlan.created_at.desc())
        .all()
    )

    teachers = db.session.query(TeacherProfile).filter_by(school_id=user.school_id).all()
    classes = db.session.query(ClassProfile).filter_by(school_id=user.school_id).all()

    teacher_ids_from_plans = {plan.teacher_id for plan in plans if plan.teacher_id}
    class_ids_from_plans = {plan.class_id for plan in plans if plan.class_id}

    extra_teachers = []
    if teacher_ids_from_plans:
        extra_teachers = (
            db.session.query(TeacherProfile)
            .filter(TeacherProfile.id.in_(teacher_ids_from_plans))
            .all()
        )

    extra_classes = []  
    if class_ids_from_plans:
        extra_classes = (
            db.session.query(ClassProfile)
            .filter(ClassProfile.id.in_(class_ids_from_plans))
            .all()
        )

    teachers_by_id = {teacher.id: teacher for teacher in teachers}
    for teacher in extra_teachers:
        teachers_by_id[teacher.id] = teacher

    classes_by_id = {class_profile.id: class_profile for class_profile in classes}
    for class_profile in extra_classes:
        classes_by_id[class_profile.id] = class_profile

    teachers = list(teachers_by_id.values())
    classes = list(classes_by_id.values())

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