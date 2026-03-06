from functools import wraps
from flask import request, jsonify
import jwt

from backend.config import SECRET_KEY, JWT_ALGORITHM


def jwt_required(f):
    """
    Access token doğrulama middleware
    """

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401

        try:
            token = auth_header.split(" ")[1]

            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[JWT_ALGORITHM]
            )

            request.user = payload

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated

def roles_required(*roles):
    """
    Role authorization middleware
    """

    def wrapper(f):

        @wraps(f)
        def decorated(*args, **kwargs):

            user = getattr(request, "user", None)

            if user is None:
                return jsonify({"error": "Unauthorized"}), 401

            if user["role"] not in roles:
                return jsonify({"error": "Forbidden"}), 403

            return f(*args, **kwargs)

        return decorated

    return wrapper