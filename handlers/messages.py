from telegram import Update
from telegram.ext import ContextTypes

from services.ai_service import ask_ai
from database import get_or_create_user
from database import get_connection


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    mode = context.user_data.get("mode")

    get_or_create_user(user_id)

    # =========================
    # TASK
    # =========================
    if mode == "task":
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (telegram_id, title) VALUES (%s, %s)",
            (user_id, text)
        )
        conn.commit()
        cur.close()
        conn.close()

        await update.message.reply_text("✅ Task saved.")
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
