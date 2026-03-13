import os
import sys

import pytest
from werkzeug.security import generate_password_hash

# Proje root'unu Python path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.extensions import db
from backend.models import School, User


@pytest.fixture
def client():
    app = create_app("testing")

    with app.app_context():
        db.create_all()

        seed_school = School(name="Seed School", address="Istanbul")
        db.session.add(seed_school)
        db.session.commit()

        admin = User(
            email="admin@test.com",
            password_hash=generate_password_hash("123456"),
            role="system_admin",
            school_id=None
        )

        school_admin = User(
            email="schooladmin@test.com",
            password_hash=generate_password_hash("123456"),
            role="school_admin",
            school_id=seed_school.id
        )

        teacher = User(
            email="teacher@test.com",
            password_hash=generate_password_hash("123456"),
            role="teacher",
            school_id=seed_school.id
        )

        db.session.add_all([admin, school_admin, teacher])
        db.session.commit()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()


def get_token(client, email, password):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    return response.get_json()["access_token"]


def test_admin_can_create_school(client):
    token = get_token(client, "admin@test.com", "123456")

    response = client.post(
        "/api/schools/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "New School", "address": "Ankara"}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "School created successfully"
    assert data["school"]["name"] == "New School"


def test_teacher_cannot_create_school(client):
    token = get_token(client, "teacher@test.com", "123456")

    response = client.post(
        "/api/schools/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Forbidden School", "address": "Izmir"}
    )

    assert response.status_code == 403
    data = response.get_json()
    assert data["error"] == "Access forbidden"


def test_school_admin_cannot_create_school(client):
    token = get_token(client, "schooladmin@test.com", "123456")

    response = client.post(
        "/api/schools/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Another School", "address": "Bursa"}
    )

    assert response.status_code == 403


def test_all_roles_can_list_schools(client):
    admin_token = get_token(client, "admin@test.com", "123456")
    school_admin_token = get_token(client, "schooladmin@test.com", "123456")
    teacher_token = get_token(client, "teacher@test.com", "123456")

    for token in [admin_token, school_admin_token, teacher_token]:
        response = client.get(
            "/api/schools/",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert isinstance(data["schools"], list)
        assert len(data["schools"]) >= 1


def test_admin_can_update_school(client):
    token = get_token(client, "admin@test.com", "123456")

    response = client.put(
        "/api/schools/1",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Updated School", "address": "Istanbul/Fatih"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "School updated successfully"
    assert data["school"]["name"] == "Updated School"


def test_school_admin_can_update_school(client):
    token = get_token(client, "schooladmin@test.com", "123456")

    response = client.put(
        "/api/schools/1",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "School Admin Updated", "address": "Istanbul/Uskudar"}
    )

    assert response.status_code == 200


def test_teacher_cannot_update_school(client):
    token = get_token(client, "teacher@test.com", "123456")

    response = client.put(
        "/api/schools/1",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Teacher Update Attempt"}
    )

    assert response.status_code == 403
    data = response.get_json()
    assert data["error"] == "Access forbidden"


def test_only_admin_can_delete_school(client):
    teacher_token = get_token(client, "teacher@test.com", "123456")
    school_admin_token = get_token(client, "schooladmin@test.com", "123456")
    admin_token = get_token(client, "admin@test.com", "123456")

    teacher_response = client.delete(
        "/api/schools/1",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    assert teacher_response.status_code == 403

    school_admin_response = client.delete(
        "/api/schools/1",
        headers={"Authorization": f"Bearer {school_admin_token}"}
    )
    assert school_admin_response.status_code == 403

    admin_response = client.delete(
        "/api/schools/1",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert admin_response.status_code == 200
    data = admin_response.get_json()
    assert data["message"] == "School deleted successfully"


def test_protected_route_without_token(client):
    response = client.get("/api/schools/")
    assert response.status_code == 401