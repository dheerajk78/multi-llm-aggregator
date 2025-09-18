from google.cloud import firestore
from datetime import datetime

db = firestore.Client()

def log_usage(user_id, provider, model, usage):
    db.collection("usage_logs").add({
        "user_id": user_id,
        "provider": provider,
        "model": model,
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0),
        "timestamp": datetime.utcnow()
    })

def save_chat(user_id, user_msg, bot_msg):
    db.collection("chat_history").add({
        "user_id": user_id,
        "user": user_msg,
        "bot": bot_msg,
        "timestamp": datetime.utcnow()
    })
