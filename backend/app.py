#backend/app.py
from flask import Flask
from flask_cors import CORS
from routes.api import api_bp
import os

def create_app():
    app = Flask(__name__)

    # CORS setup
    frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
    allowed_origins = [
        frontend_origin,
        "http://localhost:3000",   # for local React dev
        "http://127.0.0.1:3000",   # sometimes React runs here
    ]
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type", "Authorization"],
            "max_age": 3600
        }
    })

    # Register routes
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register.blueprint(auth_bp, url_prefix="/auth")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
