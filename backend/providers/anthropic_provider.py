# providers/anthropic_provider.py
from anthropic import Anthropic
from providers.base_provider import BaseLLMProvider
from firestore.firestore import save_chat, log_usage, db

class AnthropicProvider(BaseLLMProvider):
    def chat(self, user_id, message):
        try:
            client = Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                system="You are a helpful assistant.",
                messages=[{"role": "user", "content": [{"type": "text", "text": message}]}
            )

            # Anthropic responses come as list of content blocks
            reply = ""
            if response.content and len(response.content) > 0:
                reply = response.content[0].text.strip()

            if hasattr(response, "usage") and response.usage:
                log_usage(user_id, self.provider_id, self.model, {
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                })

            save_chat(user_id, message, reply)
            return {"reply": reply}

        except Exception as e:
            # structured error response
            return {"reply": f"❌ Error: {str(e)}"}

    def get_enabled_models(self):
        models_ref = db.collection("providers").document(self.provider_id).collection("models")
        models = []

        for doc in models_ref.stream():
            data = doc.to_dict()
            if data.get("enabled", False):
                models.append({
                    "id": doc.id,
                    "temperature": data.get("temperature", self.temperature)
                })
        return models

