from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider

def get_provider(provider_id, config):
    """
    Returns an instantiated provider with fully resolved model and temperature.
    """
    name = config.get("name", "").lower()
    api_key = config.get("api_key")
    model = config.get("default_model")        # resolved model from get_provider_instance
    temperature = config.get("temperature", 0.7)

    if name == "openai":
        return OpenAIProvider(
            provider_id=provider_id,
            api_key=api_key,
            model=model,
            temperature=temperature
        )
    elif name == "anthropic":
        return AnthropicProvider(
            provider_id=provider_id,
            api_key=api_key,
            model=model,
            temperature=temperature
        )
    else:
        raise ValueError(f"Unsupported provider: {name}")

def get_all_providers(include_api_key=False):
    """
    Fetch and instantiate all providers from Firestore.
    Each provider is initialized with its default model.
    """
    from firestore.firestore import db
    from providers.provider_factory import get_provider

    providers = []
    providers_ref = db.collection("providers")

    for doc in providers_ref.stream():
        data = doc.to_dict()

        if not include_api_key:
            data.pop("api_key", None)

        provider_id = doc.id

        # ✅ Resolve default model if specified
        default_model_id = data.get("default_model")

        # Fetch model doc to get temperature
        if default_model_id:
            model_doc = doc.reference.collection("models").document(default_model_id).get()
            if model_doc.exists:
                model_data = model_doc.to_dict()
                data["temperature"] = model_data.get("temperature", data.get("temperature", 0.7))
            else:
                data["temperature"] = data.get("temperature", 0.7)
        else:
            data["temperature"] = data.get("temperature", 0.7)

        # ✅ Instantiate provider
        provider_instance = get_provider(provider_id, data)
        providers.append(provider_instance)

    return providers

'''
def get_all_providers(include_api_key=False):
    """
    Fetch and instantiate all providers from Firestore.
    Each provider is initialized with its default model.
    """
    from firestore.firestore import db

    providers = []
    providers_ref = db.collection("providers")

    for doc in providers_ref.stream():
        data = doc.to_dict()
        if not include_api_key:
            data.pop("api_key", None)

        provider = get_provider(doc.id, data)
        providers.append(provider)

    return providers
'''
