from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def roles_required(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            claims = get_jwt()
            user_role = claims.get("role")

            if user_role == "system_admin":
                return func(*args, **kwargs)
            
            if user_role not in allowed_roles:
                return jsonify({"error": "Access forbidden"}), 403

            return func(*args, **kwargs)
        
        return wrapper
    return decorator