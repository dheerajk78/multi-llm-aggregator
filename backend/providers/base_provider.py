# providers/base_provider.py
from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    def __init__(self, provider_id, api_key, default_model=None, temperature=0.7):
        self.provider_id = provider_id
        self.api_key = api_key
        self.default_model = default_model  # store for dropdown
        self.model = default_model          # current active model for chat
        self.temperature = temperature
        self.name = provider_id.capitalize()

    def set_model(self, model, temperature=None):
        """Set model dynamically for chat sessions."""
        self.model = model
        if temperature is not None:
            self.temperature = temperature

    @abstractmethod
    def chat(self, user_id: str, message: str) -> dict:
        pass
