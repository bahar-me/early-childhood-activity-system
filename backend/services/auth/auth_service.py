import re
import sqlite3
from typing import Dict, Any
from datetime import datetime, timezone 
from backend.database import get_db_connection
from backend.config import SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRATION, REFRESH_TOKEN_EXPIRATION
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

ALLOWED_ROLES = {"teacher", "admin"}

 # Access token oluştur
def generate_access_token(user):
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRATION
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
            
# Refresh token oluştur
def generate_refresh_token(user):
    payload = {
        "user_id": user["id"],
        "exp": datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRATION
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

def login(email: str, password: str) -> Dict[str, Any]:
    """
    Authenticate user with email and password.
    """
    # Input validation
    if not email or not password:
        return {
            "success": False,
            "error": "Email and password are required"
        }

    # Email format kontrolü
    if not _is_valid_email(email):
        return {
            "success": False,
            "error": "Invalid email format"
        }

    try:
        with get_db_connection() as connection:
        # Email'e göre kullanıcıyı bul
            cursor = connection.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            )

            user = cursor.fetchone()

            # Kullanıcı yoksa
            if user is None:
                return {
                    "success": False,
                    "error": "Invalid credentials"
                }

            # Hash kontrolü
            if not check_password_hash(user["password"], password):
                return {
                    "success": False,
                    "error": "Invalid credentials"
                }
        token = generate_access_token(user)

        refresh_token = generate_refresh_token(user)

        # Refresh token'ı veritabanına kaydet
        connection.execute(
            "INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES (?, ?, ?)",
            (user["id"], refresh_token, datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRATION)
        )
        connection.commit()

    except Exception as e:
        print(f"Login Exception: {e}")
        return {
            "success": False,
            "error": "Something went wrong"
        }

    return {"success": True,
            "access_token": token,
            "refresh_token": refresh_token
            }

def _is_valid_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def register(email: str, password: str, role: str = "teacher") -> Dict[str, Any]:
    """
    Registers a new user in the database.
    """

    # Input validation
    if not email or not password:
        return {
            "success": False,
            "error": "Email and password are required"
        }
    if not _is_valid_email(email):
        return {
            "success": False,
            "error": "Invalid email format"
        }

    if role not in ALLOWED_ROLES:
        role = "teacher"  # Default role

    # Şifre hashleme
    hashed_password = generate_password_hash(password)

    try:
        with get_db_connection() as connection:
        # hashed_password kaydetme
            connection.execute(
                "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                (email, hashed_password, role)
            )
            connection.commit()

    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")
        return {
            "success": False,
            "error": "User already exists"
        }

    except Exception as e:
        print(f"Register Exception: {e}")
        return {
            "success": False,
            "error": "Something went wrong"
        }

    return {"success": True}

def refresh_access_token(refresh_token: str) -> Dict[str, Any]:
    if not refresh_token:
        return {"success": False, "error": "Refresh token is required"}

    try:
        # Token decode et
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = payload["user_id"]

        with get_db_connection() as connection:
            cursor = connection.execute(
                "SELECT * FROM refresh_tokens WHERE token = ?",
                (refresh_token,)
            )
            token_record = cursor.fetchone()

            # Token DB'de yoksa
            if token_record is None:
                return {"success": False, "error": "Invalid refresh token"}

            # Süresi dolmuş mu kontrol
            expires_at = token_record["expires_at"]

            if datetime.now(timezone.utc) > datetime.fromisoformat(expires_at):
                return {"success": False, "error": "Refresh token expired"}

            # Kullanıcıyı bul
            cursor = connection.execute(
                "SELECT * FROM users WHERE id = ?",
                (user_id,)
            )
            user = cursor.fetchone()

            if user is None:
                return {"success": False, "error": "User not found"}

            # Yeni access token üret
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
        with get_db_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM refresh_tokens WHERE token = ?",
                (refresh_token,)
            )

            if cursor.rowcount == 0:
                return {"success": False, "error": "Invalid refresh token"}

            connection.commit()

        return {"success": True}

    except Exception as e:
        print(f"Logout Exception: {e}")
        return {"success": False, "error": "Something went wrong"}    