from openai import AsyncOpenAI
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def clean_shopping_list(text: str, lang: str):
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You clean and organize shopping lists. Return a clear bullet list."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    return response.choices[0].message.content
