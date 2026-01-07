from openai import AsyncOpenAI
from config import OPENAI_API_KEY, AI_MODEL
from database import save_ai_message, get_ai_context

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a professional daily assistant.
Be concise, secure, and helpful.
Never generate illegal or harmful content.
"""


async def ask_smart_ai(telegram_id, prompt):
    history = get_ai_context(telegram_id)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=AI_MODEL,
        messages=messages,
        temperature=0.6,
        max_tokens=400
    )

    answer = response.choices[0].message.content

    save_ai_message(telegram_id, "user", prompt)
    save_ai_message(telegram_id, "assistant", answer)

    return answer
