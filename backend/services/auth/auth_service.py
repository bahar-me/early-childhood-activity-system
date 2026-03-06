import re
from typing import Dict, Any
from datetime import datetime, timezone

import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from backend.extensions import db
from backend.models.user import User
from backend.models.refresh_token import RefreshToken
from backend.config import (
    SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRATION,
    REFRESH_TOKEN_EXPIRATION
)

ALLOWED_ROLES = {"teacher", "school_admin", "system_admin"}


def generate_access_token(user: User) -> str:
    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "school_id": user["school_id"],
        "exp": datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRATION
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def generate_refresh_token(user: User) -> str:
    payload = {
        "user_id": user.id,
        "exp": datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRATION
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def login(email: str, password: str) -> Dict[str, Any]:

    if not email or not password:
        return {"success": False, "error": "Email and password are required"}

    if not _is_valid_email(email):
        return {"success": False, "error": "Invalid email format"}

    try:
        user = User.query.filter_by(email=email).first()

        if not user:
            return {"success": False, "error": "Invalid credentials"}

        if not check_password_hash(user.password, password):
            return {"success": False, "error": "Invalid credentials"}

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        token_record = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRATION
        )

        db.session.add(token_record)
        db.session.commit()

        return {
            "success": True,
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    except Exception as e:
        print(f"Login Exception: {e}")
        return {"success": False, "error": "Something went wrong"}


def register(email: str, password: str, role: str = "teacher", school_id: int = None) -> Dict[str, Any]:

    if not email or not password:
        return {"success": False, "error": "Email and password are required"}

    if not _is_valid_email(email):
        return {"success": False, "error": "Invalid email format"}

    if role not in ALLOWED_ROLES:
        return {"success": False, "error": "Invalid role"}

    if role in {"teacher", "school_admin"} and not school_id:
        return {"success": False, "error": "School ID is required"}

    if role == "system_admin":
        school_id = None

    try:

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return {"success": False, "error": "User already exists"}

        hashed_password = generate_password_hash(password)

        user = User(
            email=email,
            password=hashed_password,
            role=role,
            school_id=school_id
        )

        db.session.add(user)
        db.session.commit()

        return {"success": True}

    except Exception as e:
        print(f"Register Exception: {e}")
        return {"success": False, "error": "Something went wrong"}


def refresh_access_token(refresh_token: str) -> Dict[str, Any]:

    if not refresh_token:
        return {"success": False, "error": "Refresh token is required"}

    try:

        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = payload["user_id"]

        token_record = RefreshToken.query.filter_by(token=refresh_token).first()

        if not token_record:
            return {"success": False, "error": "Invalid refresh token"}

        if datetime.now(timezone.utc) > token_record.expires_at:
            return {"success": False, "error": "Refresh token expired"}

        user = User.query.get(user_id)

        if not user:
            return {"success": False, "error": "User not found"}

        new_access_token = generate_access_token(user)

        return {
            "success": True,
            "access_token": new_access_token
        }

    except jwt.ExpiredSignatureError:
        return {"success": False, "error": "Refresh token expired"}

    except jwt.InvalidTokenError:
        return {"success": False, "error": "Invalid refresh token"}

    except Exception as e:
        print(f"Refresh Exception: {e}")
        return {"success": False, "error": "Something went wrong"}


def logout(refresh_token: str) -> Dict[str, Any]:

    if not refresh_token:
        return {"success": False, "error": "Refresh token is required"}

    try:

        token_record = RefreshToken.query.filter_by(token=refresh_token).first()

        if not token_record:
            return {"success": False, "error": "Invalid refresh token"}

        db.session.delete(token_record)
        db.session.commit()

        return {"success": True}

    except Exception as e:
        print(f"Logout Exception: {e}")
        return {"success": False, "error": "Something went wrong"}


def _is_valid_email(email: str) -> bool:

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None