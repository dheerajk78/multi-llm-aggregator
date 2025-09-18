# providers/openai_provider.py
from openai import OpenAI
from .base_provider import BaseLLMProvider
from firestore import save_chat, log_usage

class OpenAIProvider(BaseLLMProvider):
    def chat(self, user_id, message):
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
