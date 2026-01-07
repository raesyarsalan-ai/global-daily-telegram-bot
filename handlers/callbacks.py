from telegram import Update
from telegram.ext import ContextTypes

from database import set_language, is_premium
from handlers.menu import main_menu
from languages import LANGUAGES


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    # =========================
    # LANGUAGE SELECTION
    # =========================
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        set_language(user_id, lang)

        await query.message.reply_text(
            LANGUAGES[lang]["start"],
            reply_markup=main_menu(lang)
        )
        return

    # =========================
    # TASKS
    # =========================
    if data == "tasks":
        await query.message.reply_text(
            "📝 Send task like:\n"
            "Buy milk | daily\n"
            "Gym | weekly\n"
            "Pay rent | monthly"
        )
        context.user_data["mode"] = "task"
        return

    # =========================
    # REMINDER
    # =========================
    if data == "add_reminder":
        await query.message.reply_text(
            "⏰ Send reminder like:\n"
            "Meeting with John | 2026-01-10 09:00"
        )
        context.user_data["mode"] = "reminder"
        return

    # =========================
    # SHOPPING
    # =========================
    if data == "shopping":
        await query.message.reply_text(
            "🛒 Send shopping items (one per line):"
        )
        context.user_data["mode"] = "shopping"
        return

    # =========================
    # AI
    # =========================
    if data == "ai":
        if not is_premium(user_id):
            await query.message.reply_text("⭐ AI is Premium-only.")
            return

        await query.message.reply_text("🤖 Ask me anything:")
        context.user_data["mode"] = "ai"
        return

    # =========================
    # PREMIUM INFO
    # =========================
    if data == "premium":
        await query.message.reply_text(
            "⭐ Premium gives you:\n"
            "- Unlimited AI\n"
            "- Smart reminders\n"
            "- Advanced scheduling"
        )
