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
# =========================
def session_guard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    return context.user_data.get("session") == get_session(user_id)


# =========================
# CALLBACK HANDLER
# =========================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not session_guard(update, context):
        await query.message.reply_text("⛔ Logged in elsewhere.")
        return

    user_id = query.from_user.id
    data = query.data

    increment_activity(user_id)

    # -------------------------
    # Daily Check-in
    # -------------------------
    if data == "daily_checkin":
        success = daily_checkin(user_id)
        streak = get_streak(user_id)

        if success:
            if streak >= 7:
                unlock_badge(user_id, "7_day_streak")

            await query.message.reply_text(
                f"✅ Check-in successful!\n🔥 Streak: {streak} days",
                reply_markup=main_menu()
            )
        else:
            await query.message.reply_text(
                "⚠️ You already checked in today.",
                reply_markup=main_menu()
            )

    # -------------------------
    # Mood Menu
    # -------------------------
    elif data == "mood_menu":
        await query.message.reply_text(
            "🧠 How are you feeling today?",
            reply_markup=mood_menu()
        )

    # -------------------------
    # Mood Selection
    # -------------------------
    elif data.startswith("mood_"):
        mood = data.replace("mood_", "")
        set_mood(user_id, mood)

        unlock_badge(user_id, "first_mood")

        await query.message.reply_text(
            f"🧠 Mood saved: {mood}",
            reply_markup=main_menu()
        )

    # -------------------------
    # Profile Summary
    # -------------------------
    elif data == "profile":
        profile = get_profile_summary(user_id)

        text = (
            "👤 Profile Summary\n\n"
            f"⭐ Premium: {profile['is_premium']}\n"
            f"📊 Activity: {profile['activity']}\n"
            f"🧠 Mood: {profile['mood']}"
        )

        if profile["activity"] >= 50:
            unlock_badge(user_id, "active_user")

        await query.message.reply_text(
            text,
            reply_markup=main_menu()
        )

    # -------------------------
    # Referral
    # -------------------------
    elif data == "referral":
        code = get_referral_code(user_id)
        if not code:
            code = generate_referral(user_id)

        unlock_badge(user_id, "referral_created")

        await query.message.reply_text(
            f"🔗 Your referral code:\n\n{code}\n\n"
            "Invite friends using this code!",
            reply_markup=main_menu()
        )

    # -------------------------
    # Back to Main
    # -------------------------
    elif data == "back_main":
        await query.message.reply_text(
            "🏠 Main Menu",
            reply_markup=main_menu()
        )

    else:
        await query.message.reply_text(
            "⚠️ Unknown action.",
            reply_markup=main_menu()
        )


# =========================
# TEXT HANDLER (fallback)
# =========================
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    increment_activity(user_id)

    await update.message.reply_text(
        "⚠️ I didn't understand that. Use the menu.",
        reply_markup=main_menu()
    )
