import os
import sys

import pytest
from werkzeug.security import generate_password_hash

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.extensions import db
from backend.models import School, User


@pytest.fixture
def client():
    app = create_app("testing")

    with app.app_context():
        db.create_all()

        school = School(name="Integration School", address="Istanbul")
        db.session.add(school)
        db.session.commit()

        teacher = User(
            email="teacher@test.com",
            password_hash=generate_password_hash("Test123!"),
            role="teacher",
            school_id=school.id,
        )
        db.session.add(teacher)
        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def auth_headers(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "teacher@test.com",
            "password": "Test123!",
        },
    )

    assert response.status_code == 200

    token = response.get_json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def activity_payload():
    return {
        "title": "Renkli Şekiller",
        "subject": "Math",
        "duration": "15-30min",
        "groupSize": "Small Group",
        "description": "Çocukların şekilleri tanımasına yönelik etkinlik.",
        "materials": ["Şekil kartları"],
        "instructions": ["Kartları göster", "Çocuklardan eşleştirme yapmalarını iste"],
        "learningGoals": ["Şekilleri tanıma"],
        "assessmentQuestions": ["Hangi şekli seçtin?"],
        "differentiationNotes": "Gerekirse daha az kart kullanılabilir.",
        "familyCommunityNotes": "Aileler evde şekil bulma oyunu oynayabilir.",
        "learningOutcomesSummary": "Çocukların şekil farkındalığı gelişir.",
    }


def test_teacher_profile_create_and_get(client):
    headers = auth_headers(client)

    create_response = client.post(
        "/api/profile/teacher",
        json={
            "name": "Ayşe Yılmaz",
            "years_experience": "4",
            "specializations": ["Matematik"],
            "teaching_style": "structured",
        },
        headers=headers,
    )

    assert create_response.status_code == 200
    assert create_response.get_json()["success"] is True

    get_response = client.get(
        "/api/profile/teacher",
        headers=headers,
    )

    assert get_response.status_code == 200
    assert get_response.get_json()["profile"]["name"] == "Ayşe Yılmaz"


def test_class_profile_create_and_get(client):
    headers = auth_headers(client)

    client.post(
        "/api/profile/teacher",
        json={
            "name": "Ayşe Yılmaz",
            "years_experience": "4",
            "specializations": ["Matematik"],
            "teaching_style": "structured",
        },
        headers=headers,
    )

    create_response = client.post(
        "/api/profile/class",
        json={
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
        headers=headers,
    )

    assert create_response.status_code == 200
    assert create_response.get_json()["success"] is True

    get_response = client.get(
        "/api/profile/class",
        headers=headers,
    )

    assert get_response.status_code == 200
    assert get_response.get_json()["class_profile"]["class_name"] == "Çiçek Sınıfı"


def test_activity_create_list_and_update(client):
    headers = auth_headers(client)

    create_response = client.post(
        "/api/activities/",
        json=activity_payload(),
        headers=headers,
    )

    assert create_response.status_code == 201

    created_activity = create_response.get_json()["activity"]
    activity_id = int(created_activity["id"])

    list_response = client.get(
        "/api/activities/?limit=20&offset=0",
        headers=headers,
    )

    assert list_response.status_code == 200
    assert list_response.get_json()["total"] >= 1

    updated_payload = activity_payload()
    updated_payload["title"] = "Güncellenmiş Şekiller"

    update_response = client.put(
        f"/api/activities/{activity_id}",
        json=updated_payload,
        headers=headers,
    )

    assert update_response.status_code == 200
    assert update_response.get_json()["activity"]["title"] == "Güncellenmiş Şekiller"


def test_activity_create_missing_required_field(client):
    headers = auth_headers(client)

    payload = activity_payload()
    del payload["title"]

    response = client.post(
        "/api/activities/",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_activity_plan_create_success(client):
    headers = auth_headers(client)

    client.post(
        "/api/profile/teacher",
        json={
            "name": "Ayşe Yılmaz",
            "years_experience": "4",
            "specializations": ["Matematik"],
            "teaching_style": "structured",
        },
        headers=headers,
    )

    client.post(
        "/api/profile/class",
        json={
            "class_name": "Çiçek Sınıfı",
            "age_group": "4-5",
            "class_size": "20",
            "learning_focus": ["Matematik"],
            "available_resources": ["Bloklar"],
            "special_needs": [],
        },
        headers=headers,
    )

    activity_response = client.post(
        "/api/activities/",
        json=activity_payload(),
        headers=headers,
    )

    activity_id = activity_response.get_json()["activity"]["id"]

    plan_response = client.post(
        "/api/activity-plans/",
        json={
            "activity_ids": [activity_id],
            "notes": "Integration test planı",
        },
        headers=headers,
    )

    assert plan_response.status_code == 201
    assert plan_response.get_json()["success"] is True


def test_activity_plan_requires_activity_ids(client):
    headers = auth_headers(client)

    client.post(
        "/api/profile/teacher",
        json={
            "name": "Ayşe Yılmaz",
            "years_experience": "4",
            "specializations": ["Matematik"],
            "teaching_style": "structured",
        },
        headers=headers,
    )

    client.post(
        "/api/profile/class",
        json={
            "class_name": "Çiçek Sınıfı",
            "age_group": "4-5",
            "class_size": "20",
            "learning_focus": ["Matematik"],
            "available_resources": ["Bloklar"],
            "special_needs": [],
        },
        headers=headers,
    )

    response = client.post(
        "/api/activity-plans/",
        json={
            "activity_ids": [],
            "notes": "Boş plan",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert "error" in response.get_json()