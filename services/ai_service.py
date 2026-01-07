from openai import AsyncOpenAI
from config import OPENAI_API_KEY, AI_MODEL

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def ask_ai(prompt: str) -> str:
    response = await client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a smart daily assistant helping users manage tasks and habits."
            },
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content
