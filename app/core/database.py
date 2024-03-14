from typing import Coroutine, Any, List, Union
from datetime import datetime
import firebase_admin
# from firebase_admin import firestore_async
from google.cloud import firestore_v1
from app.core.models import Message
from app.core.logger import logger

try:
    db = firestore_v1.AsyncClient()
    logger.info("Firebase initialized")
except Exception as e:
    logger.exception(e)
    db = None

async def fetch_messages(conversation_id: str) -> List[Union[dict, None]]:
    messages = []
    message_docs = db.collection("conversations").document(conversation_id).collection("messages").stream()
    async for doc in message_docs:
        messages.append({
            "role": doc.get("role"),
            "content": doc.get("content")
        })

    return messages

async def add_message(conversation_id: str, message: Message) -> None:
    conversation_ref = db.collection("conversations").document(conversation_id)
    conversation = await conversation_ref.get()
    if not conversation.exists:
        await conversation_ref.set({"created_at": datetime.utcnow()})

    message_ref = conversation_ref.collection("messages").document()

    await message_ref.set(message.model_dump())

async def delete_conversation(conversation_id: str) -> None:
    await db.collection("conversations").document(conversation_id).delete()
