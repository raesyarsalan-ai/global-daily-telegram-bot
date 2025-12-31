from telegram import Update
from telegram.ext import CallbackContext
from database import get_language, set_language, add_task
from languages import TEXTS
from keyboards import main_menu, language_menu
from ai import ask_ai

def t(key, lang):
    return TEXTS.get(key, {}).get(lang) or TEXTS[key]["en"]

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    lang = get_language(user_id)
    update.message.reply_text(t("start", lang), reply_markup=main_menu())

def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    lang = get_language(user_id)
    data = query.data

    if data == "language":
        query.edit_message_text("🌐 Choose language:", reply_markup=language_menu())

    elif data.startswith("lang_"):
        code = data.split("_")[1]
        set_language(user_id, code)
        query.edit_message_text("✅ Language updated", reply_markup=main_menu())

    elif data == "task":
        context.user_data["mode"] = "task"
        query.edit_message_text(t("ask_task", lang))

    elif data == "ai":
        context.user_data["mode"] = "ai"
        query.edit_message_text("🤖 Ask me anything:")

def text_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    lang = get_language(user_id)
    text = update.message.text
    mode = context.user_data.get("mode")

    if mode == "task":
        add_task(user_id, text)
        update.message.reply_text(t("task_added", lang), reply_markup=main_menu())
        context.user_data["mode"] = None

    elif mode == "ai":
        update.message.reply_text(t("ai_thinking", lang))
        reply = ask_ai(text, lang)
        update.message.reply_text(reply, reply_markup=main_menu())
