from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu
from admin import admin_panel, admin_users, admin_stats
from config import ADMIN_IDS


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    is_admin = user_id in ADMIN_IDS
    data = query.data

    if data == "admin_panel":
        await admin_panel(update, context)
        return

    if data == "admin_users":
        await admin_users(update, context)
        return

    if data == "admin_stats":
        await admin_stats(update, context)
        return

    if data == "back_menu":
        await query.message.reply_text(
            "Main Menu",
            reply_markup=main_menu(is_admin=is_admin)
        )
        return
