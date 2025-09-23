from flask import Flask
from flask_cors import CORS
from routes.api import api_bp
from routes.auth import auth_bp  # Make sure this exists
import os

def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret_key")

    # Load credentials from environment (Cloud Run secrets or local env vars)
    app.config["USERNAME"] = os.getenv("USERNAME", "admin")
    app.config["PASSWORD"] = os.getenv("PASSWORD", "password")
    
    # Session cookie config for cross-origin
    app.config.update(
        SESSION_COOKIE_SAMESITE="None",  # allow cross-site cookies
        SESSION_COOKIE_SECURE=True       # required if using HTTPS (Cloud Run)
    )

    # CORS setup
    frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
    allowed_origins = [
        frontend_origin,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # CORS for multiple route patterns
    cors_resources = {
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "max_age": 3600,
            "supports_credentials": True
        },
        r"/auth/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "max_age": 3600,
            "supports_credentials": True
        }
    }

    CORS(app, resources=cors_resources)

    # Register routes
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

