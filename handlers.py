from telegram import Update
from telegram.ext import ContextTypes

from database import (
    set_session,
    get_session,
    daily_checkin,
    get_streak,
    increment_activity,
    get_profile_summary,
    set_mood,
    generate_referral,
    get_referral_code,
    unlock_badge,
)

from keyboards import main_menu, mood_menu


# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    token = set_session(user_id)
    context.user_data["session"] = token

    increment_activity(user_id)

    await update.message.reply_text(
        "👋 Welcome back!",
        reply_markup=main_menu()
    )


# =========================
# SESSION GUARD
# =========
