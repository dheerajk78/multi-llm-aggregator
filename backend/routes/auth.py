# backend/auth.py
from flask import Blueprint, request, session, jsonify, current_app
from functools import wraps

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    valid_username = current_app.config.get("USERNAME", "admin")
    valid_password = current_app.config.get("PASSWORD", "password")

    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if username == valid_username and password == valid_password:
        session["user"] = username
        return jsonify({"success": True, "user": username})
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

