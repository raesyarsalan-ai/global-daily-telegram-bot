from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu, shopping_time_menu, tasks_menu
from languages import LANGUAGES
from ai import ask_ai
from database import (
    init_db,
    add_shopping,
    get_shopping_history,
    add_task,
    get_tasks,
    set_task_done,
    set_session,
    get_session,
)

init_db()


def get_text(key, lang):
    return LANGUAGES.get(lang, LANGUAGES["en"]).get(key, key)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    token = set_session(user_id)
    context.user_data["session"] = token

    await update.message.reply_text(
        get_text("start", "en"),
        reply_markup=main_menu()
    )


def session_guard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db_token = get_session(user_id)
    return context.user_data.get("session") == db_token


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not session_guard(update, context):
        await update.callback_query.message.reply_text("⛔ Account logged in elsewhere.")
        return

    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get("lang", "en")

    if data == "ai":
        context.user_data["mode"] = "ai"
        await query.message.reply_text(get_text("ask_ai", lang))


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not session_guard(update, context):
        await update.message.reply_text("⛔ Account logged in elsewhere.")
        return

    text = update.message.text
    mode = context.user_data.get("mode")
    lang = context.user_data.get("lang", "en")
    user_id = update.effective_user.id

    if mode == "ai":
        reply = await ask_ai(text)
        await update.message.reply_text(reply, reply_markup=main_menu())
        context.user_data["mode"] = None
        return

    await update.message.reply_text(get_text("unknown_input", lang))
