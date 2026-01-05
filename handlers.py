from telegram import Update
from telegram.ext import ContextTypes
from admin import admin_panel, admin_callback
from database import set_session, get_session
from keyboards import main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    token = set_session(user_id)
    context.user_data["session"] = token

    await update.message.reply_text(
        "Welcome 👋",
        reply_markup=main_menu()
    )


def session_guard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    return context.user_data.get("session") == get_session(user_id)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not session_guard(update, context):
        await update.callback_query.message.reply_text("⛔ Logged in elsewhere.")
        return

    data = update.callback_query.data

    if data.startswith("admin"):
        await admin_callback(update, context)
