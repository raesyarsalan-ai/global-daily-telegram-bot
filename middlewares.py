from telegram import Update
from telegram.ext import ContextTypes
from database import get_user, create_user, update_device
from security import check_rate_limit, generate_device_fingerprint
from config import DEFAULT_LANGUAGE


async def user_guard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user:
        return False

    telegram_id = update.effective_user.id

    if not check_rate_limit(telegram_id):
        await update.effective_message.reply_text("⛔ Too many requests. Try later.")
        return False

    device_fp = generate_device_fingerprint(update)
    user = get_user(telegram_id)

    if not user:
        create_user(telegram_id, DEFAULT_LANGUAGE, device_fp)
        return True

    if user["device_fingerprint"] != device_fp:
        await update.effective_message.reply_text(
            "⚠️ This account is already used on another device."
        )
        return False

    return True
