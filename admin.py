from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS
from database import get_all_users, count_users
from keyboards import admin_menu, main_menu


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.callback_query.message.reply_text("⛔ Access denied")
        return

    await update.callback_query.message.reply_text(
        "🛠 Admin Panel",
        reply_markup=admin_menu()
    )


async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_all_users()
    if not users:
        text = "No users found."
    else:
        lines = []
        for u in users:
            lines.append(f"{u[0]} | {u[1]} | {u[2]} | Premium: {u[3]}")
        text = "👥 Users:\n" + "\n".join(lines)

    await update.callback_query.message.reply_text(text, reply_markup=admin_menu())


async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = count_users()
    await update.callback_query.message.reply_text(
        f"📊 Statistics\n\nTotal users: {total}",
        reply_markup=admin_menu()
    )
