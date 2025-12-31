import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def ai_reply(text):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":text}]
    )
    return res.choices[0].message.content
