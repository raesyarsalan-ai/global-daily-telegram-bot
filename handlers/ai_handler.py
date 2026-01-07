from telegram import Update
from telegram.ext import ContextTypes
from ai.smart_ai import ask_smart_ai
from database import is_premium, increase_ai_usage

FREE_LIMIT = 5


async def ai_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if not is_premium(user_id):
        increase_ai_usage(user_id)
        if context.user_data.get("ai_used", 0) >= FREE_LIMIT:
            await update.message.reply_text("🔒 AI is Premium-only.")
            return
        context.user_data["ai_used"] = context.user_data.get("ai_used", 0) + 1

    reply = await ask_smart_ai(user_id, text)
    await update.message.reply_text(reply)
