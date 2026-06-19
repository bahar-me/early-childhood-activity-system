import os
import sys

import pytest
from werkzeug.security import generate_password_hash

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.extensions import db
from backend.models import School, User
from backend.services.profile_service import (
    upsert_teacher_profile,
    get_teacher_profile,
    upsert_class_profile,
    get_class_profile,
)


@pytest.fixture
def app_context():
    app = create_app("testing")

    with app.app_context():
        db.create_all()

        school = School(name="Profile Test School", address="Istanbul")
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


def test_upsert_teacher_profile_user_not_found(app_context):
    result = upsert_teacher_profile(9999, {"name": "Ayşe"})

    assert result["success"] is False
    assert result["error"] == "Kullanıcı bulunamadı"


def test_upsert_teacher_profile_success(app_context):
    result = upsert_teacher_profile(
        app_context.id,
        {
            "name": "Ayşe Yılmaz",
            "years_experience": "4",
            "specializations": ["Matematik"],
            "teaching_style": "structured",
        },
    )

    assert result["success"] is True
    assert result["profile"]["name"] == "Ayşe Yılmaz"


def test_get_teacher_profile_success(app_context):
    upsert_teacher_profile(
        app_context.id,
        {
            "name": "Ayşe Yılmaz",
            "years_experience": "4",
            "specializations": ["Matematik"],
            "teaching_style": "structured",
        },
    )

    result = get_teacher_profile(app_context.id)

    assert result["success"] is True
    assert result["profile"]["name"] == "Ayşe Yılmaz"


def test_get_teacher_profile_not_found(app_context):
    result = get_teacher_profile(app_context.id)

    assert result["success"] is False
    assert result["error"] == "Öğretmen profili bulunamadı"


def test_upsert_class_profile_requires_teacher_profile(app_context):
    result = upsert_class_profile(
        app_context.id,
        {
            "class_name": "Çiçek Sınıfı",
            "age_group": "4-5",
            "class_size": "20",
        },
    )

    assert result["success"] is False
    assert result["error"] == "Öğretmen profili bulunamadı"


def test_upsert_class_profile_success(app_context):
    upsert_teacher_profile(
        app_context.id,
        {
            "name": "Ayşe Yılmaz",
            "years_experience": "4",
            "specializations": ["Matematik"],
            "teaching_style": "structured",
        },
    )

    result = upsert_class_profile(
        app_context.id,
        {
            "class_name": "Çiçek Sınıfı",
            "age_group": "4-5",
            "class_size": "20",
            "learning_focus": ["Matematik"],
            "available_resources": ["Bloklar"],
            "special_needs": [],
            "daily_schedule": {
                "morning_activities": 45,
                "afternoon_activities": 30,
            },
        },
    )

    assert result["success"] is True
    assert result["class_profile"]["class_name"] == "Çiçek Sınıfı"


def test_get_class_profile_success(app_context):
    upsert_teacher_profile(
        app_context.id,
        {
            "name": "Ayşe Yılmaz",
            "years_experience": "4",
            "specializations": ["Matematik"],
            "teaching_style": "structured",
        },
    )

    upsert_class_profile(
        app_context.id,
        {
            "class_name": "Çiçek Sınıfı",
            "age_group": "4-5",
            "class_size": "20",
            "learning_focus": ["Matematik"],
            "available_resources": ["Bloklar"],
            "special_needs": [],
        },
    )

    result = get_class_profile(app_context.id)

    assert result["success"] is True
    assert result["class_profile"]["class_name"] == "Çiçek Sınıfı"


def test_get_class_profile_not_found(app_context):
    upsert_teacher_profile(
        app_context.id,
        {
            "name": "Ayşe Yılmaz",
            "years_experience": "4",
            "specializations": [],
            "teaching_style": "structured",
        },
    )

    result = get_class_profile(app_context.id)

    assert result["success"] is False
    assert result["error"] == "Sınıf profili bulunamadı"