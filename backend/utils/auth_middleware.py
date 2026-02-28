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
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])

        except Exception:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        request.user = data
        return f(*args, **kwargs)

    return decorated

def roles_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
           
            if not hasattr(request, "user"):
                return jsonify({"error": "User not authenticated."}), 401
            
            user_role = request.user.get("role")

            #system_admin her zaman erişime sahip olur
            if user_role == "system_admin":
                return f(*args, **kwargs)
            
            if user_role not in allowed_roles:
                return jsonify({"error": "Access forbidden"}), 403
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator