from openai import AsyncOpenAI
from config import OPENAI_API_KEY, AI_MODEL

# =========================
# OpenAI Client
# =========================
client = AsyncOpenAI(api_key=OPENAI_API_KEY)


# =========================
# Ask AI (Core Function)
# =========================
async def ask_ai(prompt: str) -> str:
    """
    Send prompt to OpenAI and return response text.
    Compatible with python-telegram-bot async handlers.
    """

    if not OPENAI_API_KEY:
        return "⚠️ AI service is not configured."

    try:
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful daily assistant bot."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        # لاگ واقعی در Railway دیده می‌شود
        print(f"[AI ERROR] {e}")
        return "⚠️ AI service is temporarily unavailable."
