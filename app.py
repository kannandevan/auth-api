from flask import Flask, jsonify
from routes.auth import auth_bp
from db import init_db

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route("/")
def home():
    return jsonify({"message": "Auth API running"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)