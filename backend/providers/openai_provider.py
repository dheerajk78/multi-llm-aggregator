#providers/openai_provider.py
from openai import OpenAI
from providers.base_provider import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    def chat(self, user_id, message):
        """
        Stream response from OpenAI and log usage/chat.
        Yields each chunk of text for progressive streaming.
        """
        from firestore.firestore import save_chat, log_usage
        client = OpenAI(api_key=self.api_key)
        full_text = ""
    
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message},
                ],
                temperature=self.temperature,
                stream_options={"include_usage": True}
            )
    
            # Extract text
            reply = response.choices[0].message.content
    
            # Log chat and token usage after full response
            save_chat(user_id, message, full_text)
            if hasattr(response, "usage") and response.usage:
                log_usage(
                    user_id,
                    self.provider_id,
                    self.model,
                    {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                    },
                )
        except Exception as e:
            yield f"\n[Error: {str(e)}]"
    '''
    def chat(self, user_id, message):
        from firestore.firestore import save_chat, log_usage, db

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

        if response.usage:
            log_usage(user_id, self.provider_id, self.model, {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            })

        save_chat(user_id, message, reply)
        return {"reply": reply}
'''
    def get_enabled_models(self):
        from firestore.firestore import db
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
