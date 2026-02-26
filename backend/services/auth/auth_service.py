import re
import sqlite3
from typing import Dict, Any
from datetime import datetime
from backend.database import get_db_connection
from backend.config import SECRET_KEY, JWT_EXPIRATION, JWT_ALGORITHM
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

ALLOWED_ROLES = {"teacher", "admin"}

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
            # JWT PAYLOAD oluşturma
            payload = {
                "user_id": user["id"],
                "email": user["email"],
                "role": user["role"],
                "exp": datetime.utcnow() + JWT_EXPIRATION
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

    except Exception as e:
        print(f"Login Exception: {e}")
        return {
            "success": False,
            "error": "Something went wrong"
        }

    return {"success": True,
            "token": token
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
        print(f"General Exception: {e}")
        return {
            "success": False,
            "error": "Something went wrong"
        }

    return {"success": True}