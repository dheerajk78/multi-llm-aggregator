#firestore.py
from google.cloud import firestore
import os
import requests
from datetime import datetime, timedelta
from providers.provider_factory import get_all_providers

db = firestore.Client()

def get_allowed_providers_and_models():
    providers = get_all_providers(include_api_key=False)

    result = []
    for provider in providers:
        models = provider.get_enabled_models()

        result.append({
            "id": provider.provider_id,
            "name": provider.name,
            "default_model": provider.default_model,
            "models": [
                {
                    "id": model["id"],
                    "temperature": model.get("temperature", 1.0),
                }
                for model in models
            ]
        })

    return {"providers": result}






def fetch_provider_document(provider_id):
    """Helper to get provider Firestore document or raise error."""
    provider_ref = db.collection("providers").document(provider_id)
    provider_doc = provider_ref.get()
    if not provider_doc.exists:
        raise Exception(f"Provider '{provider_id}' not found.")
    return provider_doc

def get_monthly_usage(provider_id):
    now = datetime.utcnow()
    start_of_month = datetime(now.year, now.month, 1)

    query = db.collection("usage_logs") \
              .where("provider", "==", provider_id) \
              .where("timestamp", ">=", start_of_month.isoformat())

    total_tokens = 0
    cost = 0.0

    for doc in query.stream():
        data = doc.to_dict()
        model = data["model"]
        tokens = data["total_tokens"]

        total_tokens += tokens
        cost += estimate_cost(model, tokens)

    return {
        "provider": provider_id,
        "total_tokens": total_tokens,
        "estimated_cost_usd": round(cost, 4)
    }


def estimate_cost(model, tokens):
    # Adjust as per actual prices (as of Sept 2025)
    prices = {
        "gpt-4": 0.03 / 1000,  # $0.03 per 1K tokens
        "gpt-4-32k": 0.06 / 1000,
        "gpt-3.5-turbo": 0.0015 / 1000
    }
    rate = prices.get(model, 0.002 / 1000)  # default rate
    return tokens * rate

def parse_provider(provider_doc, include_api_key=False):
    """Convert a provider document into a dict including enabled models."""
    provider_data = provider_doc.to_dict()
    provider_id = provider_doc.id

    # Get models subcollection
    models_ref = provider_doc.reference.collection("models")
    models = []
    for model_doc in models_ref.stream():
        model_data = model_doc.to_dict()
        if model_data.get("enabled", False):
            models.append({
                "id": model_doc.id,
                "temperature": model_data.get("temperature", 1.0),
                # Extend as needed
            })

    # Build result
    result = {
        "id": provider_id,
        "name": provider_data.get("name", provider_id.title()),
        "default_model": provider_data.get("default_model"),
        "models": models
    }

    if include_api_key:
        result["api_key"] = provider_data.get("api_key")

    return result


def get_provider_config(provider_id, include_api_key=True):
    """Public method to fetch config for a specific provider."""
    provider_doc = fetch_provider_document(provider_id)
    return parse_provider(provider_doc, include_api_key=include_api_key)


def get_allowed_providers_and_models():
    """Fetch all providers (no API keys), for frontend dropdowns."""
    providers_ref = db.collection("providers")
    result = []

    for provider_doc in providers_ref.stream():
        parsed = parse_provider(provider_doc, include_api_key=False)
        result.append(parsed)

    return {"providers": result}


def log_usage(user_id, provider, model, usage):
    db.collection("usage_logs").add({
        "user_id": user_id,
        "provider": provider,
        "model": model,
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0),
        "timestamp": datetime.utcnow()
    })

def save_chat(user_id, user_msg, bot_msg):
    db.collection("chat_history").add({
        "user_id": user_id,
        "user": user_msg,
        "bot": bot_msg,
        "timestamp": datetime.utcnow()
    })
