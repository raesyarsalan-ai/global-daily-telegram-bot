from telegram import Update
from telegram.ext import ContextTypes
from ai.smart_ai import ask_smart_ai
from database import is_premium
from security.abuse import check_rate_limit


async def ai_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not check_rate_limit(user_id):
        await update.message.reply_text("⏳ Too many requests. Slow down.")
        return

    if not is_premium(user_id):
        await update.message.reply_text("🔒 AI is Premium only.")
        return

    reply = await ask_smart_ai(user_id, update.message.text)
    await update.message.reply_text(reply)
