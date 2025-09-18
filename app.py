from flask import Flask
from flask_cors import CORS
from routes.api import api_bp

app = Flask(__name__)
CORS(app)  # Allow all origins (you can restrict this in production)

app.register_blueprint(api_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
