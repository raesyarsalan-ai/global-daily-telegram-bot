from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from services.ai_service import ask_ai
from services.tasks import add_task
from services.reminders import add_reminder
from scheduler import reminder_job
from database import get_or_create_user, get_connection


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    text = update.message.text.strip()
    mode = context.user_data.get("mode")

    get_or_create_user(user_id, user.username)

    # =========================
    # TASK
    # =========================
    if mode == "task":
        try:
            title, schedule = text.split("|")
            title = title.strip()
            schedule = schedule.strip().lower()

            add_task(user_id, title, schedule)
            await update.message.reply_text("✅ Task scheduled.")
        except Exception:
            await update.message.reply_text(
                "❌ Invalid format.\nExample: Gym | weekly"
            )

        context.user_data["mode"] = None
        return

    # =========================
    # REMINDER
    # =========================
    if mode == "reminder":
        try:
            body, time_str = text.split("|")
            remind_at = datetime.fromisoformat(time_str.strip())

            add_reminder(user_id, body.strip(), remind_at)

            context.application.job_queue.run_once(
                reminder_job,
                when=remind_at,
                data={
                    "telegram_id": user_id,
                    "text": body.strip()
                }
            )

            await update.message.reply_text("⏰ Reminder set successfully.")
        except Exception:
            await update.message.reply_text(
                "❌ Invalid format.\nExample:\nMeeting | 2026-01-10 09:00"
            )

        context.user_data["mode"] = None
        return

    # =========================
    # SHOPPING
    # =========================
    if mode == "shopping":
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO shopping (telegram_id, items) VALUES (%s, %s)",
            (user_id, text)
        )
        conn.commit()
        cur.close()
        conn.close()

        await update.message.reply_text("🛒 Shopping list saved.")
        context.user_data["mode"] = None
        return

    # =========================
    # AI
    # =========================
    if mode == "ai":
        reply = await ask_ai(text)
        await update.message.reply_text(reply)
        return

    # =========================
    # FALLBACK
    # =========================
    await update.message.reply_text("⚠️ Please use the menu.")
