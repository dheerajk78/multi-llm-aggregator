# backend/auth.py
from flask import Blueprint, request, session, jsonify, current_app
from functools import wraps
import jwt
import datetime

auth_bp = Blueprint("auth", __name__)
# Helper: JWT decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Unauthorized"}), 401
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user = payload["user"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

@auth_bp.route("/login", methods=["POST"])
def login():
    valid_username = current_app.config.get("USERNAME", "admin")
    valid_password = current_app.config.get("PASSWORD", "password")

    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if username == valid_username and password == valid_password:
        # Create JWT token valid for 1 hour
        token = jwt.encode({
            "user": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, current_app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify({"success": True, "token": token,  "username": username })
    return jsonify({"success": False, "error": "Invalid credentials"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"success": True})

def login_required(f):
    from flask import redirect, url_for
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function


