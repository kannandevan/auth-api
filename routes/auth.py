
from flask import Blueprint, request, jsonify
from services.auth_service import register_user_service,user_login_service,get_profile
from utils.jwt_handler import verify_token
from utils.decorators import token_required

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
    role = data.get('role')
    
    if not role:
        role = "user"
        
    result = register_user_service(username,password,role)
    
    if "error" in result:
        return jsonify(result),400
    
    return jsonify({
        "message":"User registerd",
        "data":result
    }),201
    
    
@auth_bp.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({"error":"no data provided"}),400

    username = data.get("username")
    password = data.get("password")
    
    user = user_login_service(username,password)
    
    if "error" in user:
        return jsonify(user),400
    
    return jsonify({
        "message":"login success",
        "data":user
    }),201
    
    
@auth_bp.route("/profile", methods=["GET"])
@token_required
def profile(user):
    user_id = user["user_id"]

    result = get_profile(user_id)

    if "error" in result:
        return jsonify(result), 404

    return jsonify({
        "message": "Access Granted",
        "data": result
    }), 200