# routes/api.py
from flask import Blueprint, request, jsonify
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
def chat():
    data = request.get_json()
    provider_id = data.get("provider")
    message = data.get("message")
    model = data.get("model")
    user_id = data.get("user_id", "anonymous")

    try:
        provider = get_provider_instance(provider_id)
        if model:
            provider.set_model(model)
        elif provider.default_model:
            provider.set_model(provider.default_model)
        else:
            return jsonify({"error": "No model available"}), 400

        # Stream via provider.chat() generator
        #return Response(provider.chat(user_id=user_id, message=message), content_type="text/plain")
        # Streaming generator
        def generate():
            try:
                for chunk in provider.chat(user_id=user_id, message=message):
                    yield chunk
            except Exception as e:
                # Print full traceback to Cloud Run logs
                traceback.print_exc(file=sys.stdout)
                sys.stdout.flush()  # ensure it appears in logs
                yield f"\n[Error: {str(e)}]"
        return Response(generate(), content_type="text/plain")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
