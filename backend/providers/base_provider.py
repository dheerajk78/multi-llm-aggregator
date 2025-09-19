# providers/base_provider.py
from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    def __init__(self, provider_id, api_key, model=None, temperature=0.7):
        self.provider_id = provider_id
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.name = provider_id.capitalize()

    def set_model(self, model, temperature=None):
        """Set or switch the model dynamically (used for chat sessions)."""
        self.model = model
        if temperature is not None:
            self.temperature = temperature

    @abstractmethod
    def chat(self, user_id: str, message: str) -> dict:
        pass

