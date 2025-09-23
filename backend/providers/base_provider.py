# providers/base_provider.py
from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    def __init__(self, provider_id, api_key, model, temperature=0.7, max_tokens=512):
        self.provider_id = provider_id
        self.api_key = api_key
        self.model = model          # fully resolved
        self.temperature = temperature
        self.name = provider_id.capitalize()
        # optional: store default_model for UI dropdown
        self.default_model = model
        self.max_tokens = max_tokens

    @abstractmethod
    def chat(self, user_id: str, message: str) -> dict:
        pass
