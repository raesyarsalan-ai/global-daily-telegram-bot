from telegram import Update
from telegram.ext import ContextTypes
from database import (
    get_all_users,
    set_premium_status,
)
from keyboards import admin_menu

ADMIN_IDS = [123456789]  # ← آیدی عددی ادمین خودت


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔ Access denied.")
        return

    await update.message.reply_text(
        "🛠 Admin Panel",
        reply_markup=admin_menu()
    )


async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "admin_users":
        users = get_all_users()
        text = "👥 Users:\n\n"
        for u in users:
            text += f"ID: {u['telegram_id']} | Premium: {u['is_premium']}\n"
        awa
