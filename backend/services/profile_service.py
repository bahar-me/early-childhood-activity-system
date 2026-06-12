import json
from typing import Any, Dict

from backend.extensions import db
from backend.models import TeacherProfile, ClassProfile, User


def upsert_teacher_profile(user_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
    user = db.session.get(User, user_id)
    if not user:
        return {"success": False, "error": "Kullanıcı bulunamadı"}

    profile = TeacherProfile.query.filter_by(user_id=user_id).first()

    school_id = payload.get("school_id") or user.school_id
    
    if school_id in (None, ""):
        return {"success": False, "error": "Okul bilgisi eksik"}
    
    school_id = int(school_id)

    if not profile:
        profile = TeacherProfile(user_id=user_id, school_id=school_id)
        db.session.add(profile)

    years_experience = payload.get("years_experience")
    
    profile.name = payload.get("name", "")
    profile.years_experience = int(years_experience) if years_experience not in (None, "") else 0
    profile.specializations = json.dumps(payload.get("specializations", []), ensure_ascii=False)
    profile.teaching_style = payload.get("teaching_style")
    profile.school_id = school_id
    user.school_id = school_id

    db.session.commit()
    return {"success": True, "profile": profile.to_dict()}


def get_teacher_profile(user_id: int) -> Dict[str, Any]:
    profile = TeacherProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return {"success": False, "error": "Öğretmen profili bulunamadı"}

    return {"success": True, "profile": profile.to_dict()}


def upsert_class_profile(user_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
    teacher = TeacherProfile.query.filter_by(user_id=user_id).first()
    if not teacher:
        return {"success": False, "error": "Öğretmen profili bulunamadı"}

    class_profile = ClassProfile.query.filter_by(teacher_id=teacher.id).first()
    
    if not class_profile:
        class_profile = ClassProfile(teacher_id=teacher.id, school_id=teacher.school_id)
        db.session.add(class_profile)

    class_profile.school_id = teacher.school_id  # Sınıf profili, öğretmenin okuluyla aynı okula ait olacak şekilde güncelleniyor

    class_size = payload.get("class_size")
    daily_schedule = payload.get("daily_schedule", {})

    class_profile.class_name = payload.get("class_name", "")
    class_profile.age_group = payload.get("age_group", "")
    class_profile.class_size = int(class_size) if class_size not in (None, "") else 0
    class_profile.learning_focus = json.dumps(payload.get("learning_focus", []), ensure_ascii=False)
    class_profile.available_resources = json.dumps(payload.get("available_resources", []), ensure_ascii=False)
    class_profile.special_needs = json.dumps(payload.get("special_needs", []), ensure_ascii=False)
    class_profile.morning_activities = int(daily_schedule.get("morning_activities", 45))  # Varsayılan olarak 45 dakika
    class_profile.afternoon_activities = int(daily_schedule.get("afternoon_activities", 30))  # Varsayılan olarak 30 dakika

    db.session.commit()
    return {"success": True, "class_profile": class_profile.to_dict()}


def get_class_profile(user_id: int) -> Dict[str, Any]:
    teacher = TeacherProfile.query.filter_by(user_id=user_id).first()
    if not teacher:
        return {"success": False, "error": "Öğretmen profili bulunamadı"}

    class_profile = ClassProfile.query.filter_by(teacher_id=teacher.id).first()
    if not class_profile:
        return {"success": False, "error": "Sınıf profili bulunamadı"}

    return {"success": True, "class_profile": class_profile.to_dict()}