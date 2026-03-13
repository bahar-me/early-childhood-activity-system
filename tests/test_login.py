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

        # Test verisi
        school = School(name="Test School", address="Istanbul")
        db.session.add(school)
        db.session.commit()

        teacher = User(
            email="teacher@test.com",
            password_hash=generate_password_hash("123456"),
            role="teacher",
            school_id=school.id
        )

        admin = User(
            email="admin@test.com",
            password_hash=generate_password_hash("123456"),
            role="system_admin",
            school_id=None
        )

        db.session.add(teacher)
        db.session.add(admin)
        db.session.commit()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()


def test_login_success(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "teacher@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Login successful"
    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data
    assert data["user"]["email"] == "teacher@test.com"
    assert data["user"]["role"] == "teacher"


def test_admin_login_success(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "admin@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["user"]["role"] == "system_admin"
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid_password(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "teacher@test.com",
            "password": "wrong"
        }
    )

    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data


def test_login_nonexistent_user(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nouser@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data


def test_login_missing_password(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "teacher@test.com"
        }
    )

    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data


def test_login_empty_email(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "",
            "password": "123456"
        }
    )

    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data