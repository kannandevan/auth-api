from functools import wraps
from flask import request, jsonify
from utils.jwt_handler import verify_token


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