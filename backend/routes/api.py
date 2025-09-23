# routes/api.py
from flask import Blueprint, request, jsonify, Response
from routes.auth import token_required
from firestore.firestore import (
    get_allowed_providers_and_models, get_provider_instance, get_monthly_usage
)
from providers.provider_factory import get_provider

api_bp = Blueprint("api", __name__)
@api_bp.route("/models", methods=["GET"])
def list_models():
    try:
        data = get_allowed_providers_and_models()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/usage", methods=["GET"])
def get_usage():
    provider_id = request.args.get("provider")
    return get_monthly_usage(provider_id)

@api_bp.route("/chat", methods=["POST"])
@token_required
def chat():
    data = request.get_json()
    provider_id = data.get("provider")
    message = data.get("message")
    model = data.get("model")
    user_id = getattr(request, "user", "anonymous")  # comes from JWT

    if not provider_id or not message:
        return jsonify({"error": "Missing provider or message"}), 400

    try:
        provider = get_provider_instance(provider_id, model_id=model) 
        result = provider.chat(user_id=user_id, message=message)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
