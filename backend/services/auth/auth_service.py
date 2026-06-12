from typing import Any, Dict, Optional

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from werkzeug.security import generate_password_hash, check_password_hash

from backend.extensions import db
from backend.models import RefreshToken, School, User

ALLOWED_ROLES = {"teacher", "school_admin", "system_admin"}

def _validate_email(email: str) -> bool:
    return bool(email and "@" in email and "." in email)

def _get_user_by_email(email: str) -> Optional[User]:
    return db.session.query(User).filter_by(email=email).first()

def register(email: str, password: str, role: str = "teacher", school_id: Optional[int] = None) -> Dict[str, Any]:
    if not email or not password:
        return {"success": False, "error": "Email ve şifre gereklidir"}

    if not _validate_email(email):
        return {"success": False, "error": "Geçerli bir email adresi giriniz"}

    if len(password) < 8:
        return {"success": False, "error": "Şifre en az 8 karakter olmalıdır"}

    if role not in ALLOWED_ROLES:
        return {"success": False, "error": "Geçerli bir rol seçiniz"}

    if _get_user_by_email(email):
        return {"success": False, "error": "Kullanıcı zaten mevcut"}
    
    if role in {"teacher", "school_admin"} and not school_id:
        return {"success": False, "error": "Bu rol için school_id gereklidir"}
    
    if role == "system_admin":
        school_id = None

    school = None
    if school_id:
        school = db.session.get(School, school_id)
        if not school:
            return {"success": False, "error": "Okul bulunamadı"}
        
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
        return {"success": False, "error": "Email ve şifre gereklidir"}

    user = _get_user_by_email(email)
    if not user:
        return {"success": False, "error": "Geçersiz kimlik bilgileri"}

    if not check_password_hash(user.password_hash, password):
        return {"success": False, "error": "Geçersiz kimlik bilgileri"}

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
        return {"success": False, "error": "Refresh token gereklidir"}

    stored_token = db.session.query(RefreshToken).filter_by(token=refresh_token, is_revoked=False).first()
    if not stored_token:
        return {"success": False, "error": "Geçersiz veya iptal edilmiş refresh token"}

    try:
        payload = decode_token(refresh_token)
        user_id = int(payload["sub"])
    except Exception:
        return {"success": False, "error": "Geçersiz veya süresi dolmuş refresh token"}

    user = db.session.get(User, user_id)    
    if not user:
        return {"success": False, "error": "Kullanıcı bulunamadı"}

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
        return {"success": False, "error": "Refresh token gereklidir"}

    token_record = db.session.query(RefreshToken).filter_by(token=refresh_token, is_revoked=False).first()
    if not token_record:
        return {"success": False, "error": "Geçersiz refresh token"}

    token_record.is_revoked = True
    db.session.commit()

    return {"success": True, "message": "Çıkış başarılı"}