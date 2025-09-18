from flask import Flask
from flask_cors import CORS
from routes.api import api_bp
import os

frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

app = Flask(__name__)
CORS(app)  # Allow all origins (you can restrict this in production)

app.register_blueprint(api_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

def create_app():
    app = Flask(__name__)

    # Only allow your deployed frontend to call API
    CORS(app, resources={
        r"/api/*": {
            "origins": "https://llm-frontend-753300783805.australia-southeast1.run.app"
        }
    })

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
