from fastapi import APIRouter, HTTPException, Body
from typing import List, Optional, Union
import os

from app.core.database import *
from app.core.agent import process_incoming_message

router = APIRouter()

@router.post('/chat/{id}')
async def process_message(id: str, level: str, message: str, api_key: Optional[str] = Body(default=None)) -> Union[Message, None]:
    try:
        if message == "conversation:reset":
            await delete_conversation(f"{id}-{level}")
            return

        if not api_key or "" == api_key:
            if not level == "easy":
                raise(HTTPException(status_code=401, detail="API key required"))
            api_key = os.getenv("OPENAI_API_KEY")

        response = await process_incoming_message(id, level, message, api_key)
        return response
    except Exception as e:
        raise HTTPException(status_code=500)


@router.get('/chat/{id}')
async def get_messages(id: str, level: str) -> List[Message]:
    conversation_id = f"{id}-{level}"
    messages = await fetch_messages(conversation_id)
    return messages

