from telegram import Update
from telegram.ext import ContextTypes

from ai.ask_ai import ask_ai
from database import (
    add_task,
    get_tasks,
    set_task_done,
    add_shopping,
    get_shopping_history,
    get_preferences,
)
from database.subscription import is_premium
from weather import weather_by_coords


# =========================
# USER MODE KEYS
# =========================
MODE_AI = "mode_ai"
MODE_TASK = "mode_task"
MODE_SHOPPING = "mode_shopping"
MODE_REMINDER = "mode_reminder"
MODE_WEATHER = "mode_weather"


# =========================
# MAIN TEXT HANDLER
# =========================
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip()
    user_id = user.id

    # Current mode
    mode = context.user_data.get("mode")

    # =========================
    # AI MODE
    # =========================
    if mode == MODE_AI:
        # Premium guard
        if not is_premium(user_id):
            await update.message.reply_text(
                "⭐ AI Assistant is a Premium feature.\n"
                "Upgrade to Premium to continue."
            )
            return

        try:
            reply = await ask_ai(text)
            await update.message.reply_text(reply)
        except Exception as e:
            await update.message.reply_text("⚠️ AI service is temporarily unavailable.")
        return

    # =========================
    # TASK MODE
    # =========================
    if mode == MODE_TASK:
        if text.lower().startswith("done"):
            try:
                task_id = int(text.split()[-1])
                set_task_done(user_id, task_id)
                await update.message.reply_text("✅ Task marked as done.")
            except Exception:
                await update.message.reply_text("❌ Invalid task ID.")
            return

        add_task(user_id, text)
        await update.message.reply_text("📝 Task added.")
        return

    # =========================
    # SHOPPING MODE
    # =========================
    if mode == MODE_SHOPPING:
        items = [line.strip() for line in text.split("\n") if line.strip()]
        if not items:
            await update.message.reply_text("❌ Shopping list is empty.")
            return

        add_shopping(user_id, "\n".join(items), None)
        await update.message.reply_text("🛒 Shopping list saved.")
        return

    # =========================
    # REMINDER MODE
    # =========================
    if mode == MODE_REMINDER:
        # Placeholder for advanced reminder parsing
        await update.message.reply_text(
            "⏰ Reminder saved.\n"
            "You will be notified at the scheduled time."
        )
        return

    # =========================
    # WEATHER MODE
    # =========================
    if mode == MODE_WEATHER:
        if not update.message.location:
            await update.message.reply_text("📍 Please send your location.")
            return

        lat = update.message.location.latitude
        lon = update.message.location.longitude

        try:
            weather = weather_by_coords(lat, lon)
            await update.message.reply_text(f"🌤 Weather:\n{weather}")
        except Exception:
            await update.message.reply_text("⚠️ Weather service unavailable.")
        return

    # =========================
    # DEFAULT FALLBACK
    # =========================
    await update.message.reply_text(
        "🤖 Please choose an option from the menu.\n"
        "Use /start to open the main menu."
    )
