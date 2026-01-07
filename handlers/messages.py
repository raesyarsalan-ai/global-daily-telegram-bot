from telegram import Update
from telegram.ext import ContextTypes

from ai import ask_ai
from languages import LANGUAGES


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    user_data = context.user_data

    lang = user_data.get("lang", "en")
    texts = LANGUAGES.get(lang, LANGUAGES["en"])

    if user_data.get("state") == "ASK_AI":
        await update.message.chat.send_action("typing")

        try:
            reply = await ask_ai(user_text)
        except Exception:
            reply = "⚠️ AI service is temporarily unavailable."

        user_data["state"] = None
        await update.message.reply_text(reply)
        return

    await update.message.reply_text(texts["unknown_input"])
