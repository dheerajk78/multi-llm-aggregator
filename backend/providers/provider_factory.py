# providers/provider_factory.py
from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider

def get_provider(provider_id, config):
    name = config.get("name", "").lower()
    api_key = config.get("api_key")
    default_model = config.get("default_model")
    temperature = config.get("temperature", 0.7)

    if name == "openai":
        return OpenAIProvider(provider_id=provider_id, api_key=api_key,
                              default_model=default_model, temperature=temperature)
    elif name == "anthropic":
        return AnthropicProvider(provider_id=provider_id, api_key=api_key,
                                 default_model=default_model, temperature=temperature)
    else:
        raise ValueError(f"Unsupported provider: {name}")


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
