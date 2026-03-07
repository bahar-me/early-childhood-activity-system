
import os
import sys

import pytest

# Proje root'unu Python path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.extensions import db
from backend.models import School, User
from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    app = create_app("testing")

    with app.app_context():
        db.create_all()

        # Test verisi ekle
        school = School(name="Test School", address="Istanbul")
        db.session.add(school)
        db.session.commit()

        user = User(
            email="teacher@test.com",
            password_hash=generate_password_hash("123456"),
            role="teacher",
            school_id=school.id
        )
        db.session.add(user)
        db.session.commit()


        with app.test_client() as client:
            yield client

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


def test_login_invalid_password(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "teacher@test.com",
            "password": "wrong"
        }
    )
    assert response.status_code == 401


def test_login_missing_fields(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": ""
        }
    )
    assert response.status_code == 401