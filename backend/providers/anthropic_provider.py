# providers/anthropic_provider.py
from .base_provider import BaseLLMProvider
from backend.firestore.firestore import save_chat, log_usage
import anthropic

class AnthropicProvider(BaseLLMProvider):
    def chat(self, user_id, message):
        client = anthropic.Anthropic(api_key=self.api_key)

        response = client.messages.create(
            model=self.model,
            max_tokens=1024,
            temperature=self.temperature,
            messages=[{"role": "user", "content": message}]
        )

        reply = response.content[0].text

        # Simulated usage logging (Anthropic doesn't always return usage)
        log_usage(user_id, self.provider_id, self.model, {
            "prompt_tokens": 100,
            "completion_tokens": 500,
            "total_tokens": 600
        })

        save_chat(user_id, message, reply)

        return {"reply": reply}
