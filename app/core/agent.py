from app.core.logger import logger
from app.core.database import *
from app.core.models import *
from app.core.llm.prompts import *
from app.core.llm.openai import *


async def process_incoming_message(user_id: str, level: str, message: str, api_key: str) -> Message:
    conversation_id = f"{user_id}-{level}"

    try:
        await add_message(conversation_id, Message(content=message, role="user"))

        messages = await fetch_messages(conversation_id)

        config = get_config(level)

        system_message = {
            "role": "system",
            "content": config["prompt"]
        }

        messages.insert(0, system_message)

        response = await get_async_completion(messages, api_key, config["model"])

        resp_message = Message(content=response, role="assistant")
        await add_message(conversation_id, resp_message)

        return resp_message

        
    except Exception as e:
        logger.exception(e)
        return 