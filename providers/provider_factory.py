# providers/provider_factory.py
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider

def get_provider(provider_id, config):
    name = config.get("name", "").lower()
    api_key = config.get("api_key")
    model = config.get("default_model")
    temperature = config.get("temperature", 0.7)

    if name == "openai":
        return OpenAIProvider(provider_id, api_key, model, temperature)
    elif name == "anthropic":
        return AnthropicProvider(provider_id, api_key, model, temperature)
    else:
        raise ValueError(f"Unsupported provider: {name}")
