from functools import wraps
from flask import request, jsonify
from utils.jwt_handler import verify_token
from db import get_user_by_id


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token missing"}), 401

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 401

        decoded = verify_token(token)

        if "error" in decoded:
            return jsonify(decoded), 401

        # pass user info to route
        return f(decoded, *args, **kwargs)

    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(user, *args, **kwargs):

        user_id = user.get("user_id")

        db_user = get_user_by_id(user_id)

        if not db_user:
            return jsonify({"error": "User not found"}), 404

        if db_user.get("role") != "admin":
            return jsonify({"error": "Forbidden: Admins only"}), 403

        return f(user, *args, **kwargs)

    return wrapper