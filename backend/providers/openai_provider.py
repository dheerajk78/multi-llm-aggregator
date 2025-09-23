from openai import OpenAI
from providers.base_provider import BaseLLMProvider
from firestore.firestore import save_chat, log_usage, db

class OpenAIProvider(BaseLLMProvider):
    def chat(self, user_id, message):
        try:
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message}
                ]
            )

            reply = response.choices[0].message.content

            if hasattr(response, "usage") and response.usage:
                log_usage(user_id, self.provider_id, self.model, {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
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

