from telegram import Update
from telegram.ext import ContextTypes
from database.subscription import is_premium


async def premium_guard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_premium(user_id):
        await update.message.reply_text(
            "⭐ This feature is Premium only.\nUse /premium to upgrade."
        )
        return False

    return True
