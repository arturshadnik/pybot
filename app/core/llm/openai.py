from typing import List
from openai import AsyncOpenAI

async def get_async_completion(messages: List[dict], api_key: str, model: str='gpt-3.5-turbo') -> str:
    aclient = AsyncOpenAI()

    response = await aclient.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        max_tokens=200
    )
    return response.choices[0].message.content
