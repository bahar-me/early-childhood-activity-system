import jwt
from functools import wraps
from flask import request, jsonify
from backend.config import SECRET_KEY, JWT_ALGORITHM


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token is missing"}), 401
        
        try:
            parts = auth_header.split()

            if len(parts) != 2 or parts[0] != "Bearer":
                return jsonify({"error": "Invalid token format"}), 401

            token = parts[1]

            data = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[JWT_ALGORITHM]
            )

            request.user = data

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Token is invalid"}), 401

        except Exception as e:
            print(f"Auth Middleware Exception: {e}")
            return jsonify({"error": "Authentication error"}), 401

        return f(*args, **kwargs)

    return decorated

def role_required(required_role):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = getattr(request, "user", None)

            if not user:
                return jsonify({"error": "Authentication required"}), 401
            
            if user.get("role") != required_role:
                return jsonify({"error": "Access forbidden"}), 403
            
            return f(*args, **kwargs)
        
        return decorated
    
    return wrapper