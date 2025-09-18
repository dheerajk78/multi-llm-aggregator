# routes/api.py
from flask import Blueprint, request, jsonify
from firestore import get_provider_config
from providers.provider_factory import get_provider

api_bp = Blueprint("api", __name__)

@api_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    provider_id = data.get("provider")
    message = data.get("message")
    user_id = data.get("user_id", "anonymous")

    try:
        config = get_provider_config(provider_id, include_api_key=True)
        provider = get_provider(provider_id, config)
        result = provider.chat(user_id=user_id, message=message)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
