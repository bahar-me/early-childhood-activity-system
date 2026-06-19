import os
import sys

import pytest
from werkzeug.security import generate_password_hash

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.extensions import db
from backend.models import School, User
from backend.services.auth.auth_service import login


@pytest.fixture
def app_context():
    app = create_app("testing")

    with app.app_context():
        db.create_all()

        school = School(name="Auth Unit School", address="Istanbul")
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

        yield app

        db.session.remove()
        db.drop_all()


def test_login_success(app_context):
    result = login("teacher@test.com", "Test123!")

    assert result["success"] is True
    assert "access_token" in result
    assert "refresh_token" in result
    assert result["user"]["email"] == "teacher@test.com"


def test_login_invalid_password(app_context):
    result = login("teacher@test.com", "WrongPassword")

    assert result["success"] is False
    assert "error" in result


def test_login_user_not_found(app_context):
    result = login("missing@test.com", "Test123!")

    assert result["success"] is False
    assert "error" in result


def test_login_empty_email(app_context):
    result = login("", "Test123!")

    assert result["success"] is False
    assert "error" in result


def test_login_empty_password(app_context):
    result = login("teacher@test.com", "")

    assert result["success"] is False
    assert "error" in result