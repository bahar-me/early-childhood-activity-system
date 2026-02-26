
import pytest
import sys
import os

# Proje root'unu Python path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_success(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "teacher@test.com",
            "password": "123456"
        }
    )
    assert response.status_code == 200
    assert b"Login successful" in response.data


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