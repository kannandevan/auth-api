


def validate_register_input(username,password,role):
    if not isinstance(username, str) or not username.strip():
        return {"error": "Invalid username"}

    if not isinstance(password, str) or len(password) < 6:
        return {"error": "Password must be at least 6 characters"}
    
    username = username.strip().lower()
    
    
    return{"username":username,"password":password}