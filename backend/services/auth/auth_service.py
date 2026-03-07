from datetime import datetime, timezone
from typing import Any, Dict, Optional

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from werkzeug.security import generate_password_hash, check_password_hash

from backend.extensions import db
from backend.models import RefreshToken, School, User

ALLOWED_ROLES = {"teacher", "school_admin", "system_admin"}

def _validate_email(email: str) -> bool:
    return bool(email and "@" in email and "." in email)

def _get_user_by_email(email: str) -> Optional[User]:
    return User.query.filter_by(email=email).first()

def register(email: str, password: str, role: str = "teacher", school_id: Optional[int] = None) -> Dict[str, Any]:
    if not email or not password:
        return {"success": False, "error": "Email and password are required"}

    if not _validate_email(email):
        return {"success": False, "error": "Invalid email format"}

    if role not in ALLOWED_ROLES:
        return {"success": False, "error": "Invalid role"}

    if _get_user_by_email(email):
        return {"success": False, "error": "User already exists"}
    
    if role in {"teacher", "school_admin"} and not school_id:
        return {"success": False, "error": "School ID is required for this role"}
    
    if role == "system_admin":
        school_id = None

    school = None
    if school_id:
        school = School.query.get(school_id)
        if not school:
            return {"success": False, "error": "School not found"}
        
    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        school_id=school_id if school_id else None
    )

    db.session.add(user)
    db.session.commit()

    return {"success": True, "user": user.to_dict()}

def login(email: str, password: str) -> Dict[str, Any]:
    if not email or not password:
        return {"success": False, "error": "Email and password are required"}

    user = _get_user_by_email(email)
    if not user:
        return {"success": False, "error": "Invalid credentials"}

    if not check_password_hash(user.password_hash, password):
        return {"success": False, "error": "Invalid credentials"}

    additional_claims = {
        "role": user.role,
        "school_id": user.school_id
    }
    access_token = create_access_token(
        identity=str(user.id), 
        additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(identity=str(user.id))
    refresh_token_record = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        is_revoked=False
    )
    db.session.add(refresh_token_record)
    db.session.commit()

    return {
        "success": True,    
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }

def refresh_access_token(refresh_token: str) -> Dict[str, Any]:
    if not refresh_token:
        return {"success": False, "error": "Refresh token is required"}

    stored_token = RefreshToken.query.filter_by(token=refresh_token, is_revoked=False).first()
    if not stored_token:
        return {"success": False, "error": "Invalid or revoked refresh token"}
    
    try:
        payload = decode_token(refresh_token)
        user_id = int(payload["sub"])
    except Exception:
        return {"success": False, "error": "Invalid or expired refresh token"}

    user = User.query.get(user_id)
    if not user:
        return {"success": False, "error": "User not found"}

    new_access_token = create_access_token(
        identity=str(user.id), 
        additional_claims={
            "role": user.role,
            "school_id": user.school_id
        }
    )

    return {
        "success": True,
        "access_token": new_access_token
    }

def logout(refresh_token: str) -> Dict[str, Any]:
    if not refresh_token:
        return {"success": False, "error": "Refresh token is required"}

    token_record = RefreshToken.query.filter_by(token=refresh_token, is_revoked=False).first()
    if not token_record:
        return {"success": False, "error": "Invalid refresh token"}

    token_record.is_revoked = True
    db.session.commit()

    return {"success": True, "message": "Logged out successfully"}