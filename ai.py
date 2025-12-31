import openai
from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

async def chat_ai(prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()
