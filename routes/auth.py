
from flask import Blueprint, request, jsonify
from services.auth_service import register_user_service,user_login_service,get_profile,get_all_users_service
from utils.decorators import token_required,admin_required
from utils.validators import validate_register_input
from utils.response import success_response,error_response

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/test")
def test():
    return success_response("Auth route working","dummy_data",200)


@auth_bp.route("/register",methods=["POST"])
def register():
    data =request.get_json()
    
    if not data:
        return error_response("no data provided",400)

    username = data.get("username")
    password = data.get("password")

    
    role = "user"
    credentials = validate_register_input(username,password)
    if "error" in credentials:
         return error_response(credentials["error"],400)
    
    verified_username = credentials["username"]
    verified_password = credentials["password"]
    
    
      
    result = register_user_service(verified_username,verified_password,role)
    
    if "error" in result:
        return error_response(result["error"],400)
    
    return success_response("User registered",result,201)
    
    
@auth_bp.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    
    if not data:
        return error_response("no data provided",400)

    username = data.get("username")
    password = data.get("password")
    
    user = user_login_service(username,password)
    
    if "error" in user:
        return error_response(user["error"],400)
    
    return success_response("login success",user,200)

    
    
@auth_bp.route("/profile", methods=["GET"])
@token_required
def profile(user):
    user_id = user["user_id"]

    result = get_profile(user_id)

    if "error" in result:
        return error_response(result["error"],404)

    return success_response("Access Granted",result,200)
    
    
@auth_bp.route("/admin/users", methods=["GET"])
@token_required
@admin_required
def get_all_users(user):

    users = get_all_users_service()

    return success_response("All users",users,200)