from openai import AsyncOpenAI
from config import OPENAI_API_KEY
import json

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def ask_ai(prompt: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful daily assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


async def parse_shopping_text(text: str) -> dict:
    prompt = f"""
Extract shopping items and reminder datetime from the text.
Return ONLY valid JSON.

Text:
{text}

Format:
{{
  "items": ["item1", "item2"],
  "remind_at": "YYYY-MM-DD HH:MM"
}}
"""
    response = await ask_ai(prompt)
    return json.loads(response)
