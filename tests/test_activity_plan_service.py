import os
import sys

import pytest
from werkzeug.security import generate_password_hash

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.extensions import db
from backend.models import School, User, TeacherProfile, ClassProfile
from backend.services.activity_plan_service import create_activity_plan


@pytest.fixture
def app_context():
    app = create_app("testing")

    with app.app_context():
        db.create_all()

        school = School(name="Plan Test School", address="Istanbul")
        db.session.add(school)
        db.session.commit()

        user = User(
            email="teacher@test.com",
            password_hash=generate_password_hash("Test123!"),
            role="teacher",
            school_id=school.id,
        )
        db.session.add(user)
        db.session.commit()

        yield user

        db.session.remove()
        db.drop_all()


def test_create_activity_plan_requires_teacher_profile(app_context):
    result = create_activity_plan(
        app_context.id,
        {"activity_ids": ["1"], "notes": "Test planı"},
    )

    assert result["success"] is False
    assert result["error"] == "Öğretmen profili bulunamadı"


def test_create_activity_plan_requires_class_profile(app_context):
    teacher = TeacherProfile(
        user_id=app_context.id,
        school_id=app_context.school_id,
        name="Ayşe Yılmaz",
        years_experience=4,
        specializations="[]",
        teaching_style="structured",
    )
    db.session.add(teacher)
    db.session.commit()

    result = create_activity_plan(
        app_context.id,
        {"activity_ids": ["1"], "notes": "Test planı"},
    )

    assert result["success"] is False
    assert result["error"] == "Sınıf profili bulunamadı"


def test_create_activity_plan_requires_activity_ids(app_context):
    teacher = TeacherProfile(
        user_id=app_context.id,
        school_id=app_context.school_id,
        name="Ayşe Yılmaz",
        years_experience=4,
        specializations="[]",
        teaching_style="structured",
    )
    db.session.add(teacher)
    db.session.commit()

    class_profile = ClassProfile(
        teacher_id=teacher.id,
        school_id=app_context.school_id,
        class_name="Çiçek Sınıfı",
        age_group="4-5",
        class_size=20,
        learning_focus="[]",
        available_resources="[]",
        special_needs="[]",
        morning_activities=45,
        afternoon_activities=30,
    )
    db.session.add(class_profile)
    db.session.commit()

    result = create_activity_plan(
        app_context.id,
        {"activity_ids": [], "notes": "Boş plan"},
    )

    assert result["success"] is False
    assert result["error"] == "En az bir etkinlik gereklidir"


def test_create_activity_plan_success(app_context):
    teacher = TeacherProfile(
        user_id=app_context.id,
        school_id=app_context.school_id,
        name="Ayşe Yılmaz",
        years_experience=4,
        specializations="[]",
        teaching_style="structured",
    )
    db.session.add(teacher)
    db.session.commit()

    class_profile = ClassProfile(
        teacher_id=teacher.id,
        school_id=app_context.school_id,
        class_name="Çiçek Sınıfı",
        age_group="4-5",
        class_size=20,
        learning_focus="[]",
        available_resources="[]",
        special_needs="[]",
        morning_activities=45,
        afternoon_activities=30,
    )
    db.session.add(class_profile)
    db.session.commit()

    result = create_activity_plan(
        app_context.id,
        {"activity_ids": ["1", "2"], "notes": "Test planı"},
    )

    assert result["success"] is True
    assert result["plan"]["notes"] == "Test planı"