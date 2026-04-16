import bcrypt
from db import create_user_db,get_user_by_username,get_user_by_id
from utils.jwt_handler import generate_token

def register_user_service(username,password,role="user"):
    if not isinstance(username, str) or not username.strip():
        return {"error": "Invalid username"}

    if not isinstance(password, str) or len(password) < 6:
        return {"error": "Password must be at least 6 characters"}

    username = username.strip().lower()
    role = role.strip().lower()

    # hash password
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    result = create_user_db(username, hashed.decode("utf-8"),role)

    if not result or result is None:
        return {"error": "Username already exists"}

    return result


def user_login_service(username,password):
    
    user = get_user_by_username(username)
    if not  user:
        return {"error":"user not found"}
    
    
    if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return {"error":"incorrect password"}
    
    token = generate_token(user["id"])

    return {
        "id": user["id"],
        "username": user["username"],
        "token": token
    }
    
def get_profile(user_id):
    
    user = get_user_by_id(user_id)
    if not  user:
        return {"error":"user not found"}
    
    return {
        "id": user["id"],
        "username": user["username"],
        "role":user["role"]
    }
    