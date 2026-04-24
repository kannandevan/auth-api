
from flask import  jsonify

def success_response(message,data,status_code):
    return jsonify({"success":True,"message":message,"data":data}),status_code

def error_response(message,status_code):
    return jsonify({"success":False,"message":message,"data":None}),status_code