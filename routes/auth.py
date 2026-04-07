
from flask import Blueprint, request, jsonify
from services.auth_service import register_user_service
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/test")
def test():
    return jsonify({"message": "Auth route working"})


@auth_bp.route("/register",methods=["POST"])
def regsiter():
    data =request.get_json()
    
    if not data:
        return jsonify({"error":"no data provided"}),400

    username = data.get("username")
    password = data.get("password")
    
    result = register_user_service(username,password)
    
    if "error" in result:
        return jsonify(result),400
    
    return jsonify({
        "message":"User registerd",
        "data":result
    }),201