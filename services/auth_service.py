import bcrypt
from db import create_user_db

def register_user_service(username,password):
    if not isinstance(username, str) or not username.strip():
        return {"error": "Invalid username"}

    if not isinstance(password, str) or len(password) < 6:
        return {"error": "Password must be at least 6 characters"}

    username = username.strip().lower()

    # hash password
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    result = create_user_db(username, hashed.decode("utf-8"))

    if not result or result is None:
        return {"error": "Username already exists"}

    return result