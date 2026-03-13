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

        school = School(name="Flow School", address="Istanbul")
        db.session.add(school)
        db.session.commit()

        teacher = User(
            email="teacher@test.com",
            password_hash=generate_password_hash("123456"),
            role="teacher",
            school_id=school.id
        )
        db.session.add(teacher)
        db.session.commit()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()


def login_and_get_tokens(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "teacher@test.com", "password": "123456"}
    )
    assert response.status_code == 200

    data = response.get_json()
    return data["access_token"], data["refresh_token"]


def test_refresh_token_success(client):
    _, refresh_token = login_and_get_tokens(client)

    response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Access token refreshed"
    assert "access_token" in data


def test_logout_success(client):
    _, refresh_token = login_and_get_tokens(client)

    response = client.post(
        "/api/auth/logout",
        json={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Logged out successfully"


def test_refresh_fails_after_logout(client):
    _, refresh_token = login_and_get_tokens(client)

    logout_response = client.post(
        "/api/auth/logout",
        json={"refresh_token": refresh_token}
    )
    assert logout_response.status_code == 200

    refresh_response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token}
    )

    assert refresh_response.status_code == 401
    data = refresh_response.get_json()
    assert "error" in data


def test_refresh_with_invalid_token(client):
    response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": "fake.invalid.token"}
    )

    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data


def test_logout_with_invalid_token(client):
    response = client.post(
        "/api/auth/logout",
        json={"refresh_token": "fake.invalid.token"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data