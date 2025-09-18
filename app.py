from flask import Flask
from flask_cors import CORS
from routes.api import api_bp
import os

frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

def create_app():
    app = Flask(__name__)

    # Only allow your deployed frontend to call API
    CORS(app, resources={
    r"/api/*": {
        "origins": [frontend_origin],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"],
        "max_age": 3600
        }
    })

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app

# 👇 This line is required so gunicorn (or any WSGI server) can find the app
app = create_app()
