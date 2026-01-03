from openai import AsyncOpenAI
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def ask_ai(prompt: str) -> str:
    res = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a smart daily assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return res.choices[0].message.content
