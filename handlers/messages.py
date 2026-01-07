from telegram import Update
from telegram.ext import ContextTypes

from ai import ask_ai
from languages import LANGUAGES


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    user_data = context.user_data

    # زبان کاربر (پیش‌فرض انگلیسی)
    lang = user_data.get("lang", "en")
    texts = LANGUAGES.get(lang, LANGUAGES["en"])

    # اگر کاربر در حالت سوال از AI است
    if user_data.get("state") == "ASK_AI":
        await update.message.chat.send_action("typing")

        try:
            ai_response = await ask_ai(user_text)
        except Exception as e:
            ai_response = "⚠️ AI service is temporarily unavailable."

        user_data["state"] = None
        await update.message.reply_text(ai_response)
        return

    # ورودی ناشناخته
    await update.message.reply_text(texts["unknown_input"])
