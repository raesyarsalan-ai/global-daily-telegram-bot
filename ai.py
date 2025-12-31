from openai import OpenAI
from config import OPENAI_API_KEY, AI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a smart, friendly daily assistant.
Help users with tasks, productivity, daily planning, and motivation.
Be concise and practical.
"""

def ask_ai(user_text: str, language: str = "en") -> str:
    try:
        res = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return res.choices[0].message.content
    except Exception:
        return "⚠️ AI is temporarily unavailable."
