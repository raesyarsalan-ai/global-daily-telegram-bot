from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu, shopping_time_menu, tasks_menu
from languages import LANGUAGES
from ai import ask_ai
import uuid

from database import (
    init_db,
    add_shopping,
    get_shopping_history,
    add_task,
    get_tasks,
    set_task_done,
    save_session,
    get_session
)

# Initialize database
init_db()


def get_text(key: str, lang: str):
    return LANGUAGES.get(lang, LANGUAGES["en"]).get(key, key)


def validate_session(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    telegram_id = update.effective_user.id
    current_session = context.user_data.get("session_id")
    db_session = get_session(telegram_id)
    return current_session and current_session == db_session


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    username = update.effective_user.username or ""
    lang = context.user_data.get("lang", "en")

    session_id = str(uuid.uuid4())
    context.user_data["session_id"] = session_id

    save_session(telegram_id, session_id, username)

    await update.message.reply_text(
        get_text("start", lang),
        reply_markup=main_menu()
    )


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not validate_session(update, context):
        await query.message.reply_text("⚠️ Your session has expired. Please /start again.")
        return

    user_id = query.from_user.id
    lang = context.user_data.get("lang", "en")
    data = query.data

    if data.startswith("lang_"):
        new_lang = data.split("_")[1]
        context.user_data["lang"] = new_lang
        await query.message.reply_text(
            get_text("language_changed", new_lang),
            reply_markup=main_menu()
        )
        return

    if data == "ai":
        context.user_data["mode"] = "ai_chat"
        await query.message.reply_text(get_text("ask_ai", lang))
        return

    if data == "shopping":
        context.user_data["mode"] = "shopping_items"
        await query.message.reply_text(get_text("ask_shopping", lang))
        return

    if data == "shop_today":
        items = context.user_data.pop("shopping_items", [])
        add_shopping(user_id, "\n".join(items), "today")
        await query.message.reply_text(
            get_text("shopping_saved_today", lang),
            reply_markup=main_menu()
        )
        return

    if data == "shop_later":
        context.user_data["mode"] = "shopping_time"
        await query.message.reply_text(get_text("ask_shopping_time", lang))
        return

    if data == "shop_history":
        history = get_shopping_history(user_id)
        if not history:
            await query.message.reply_text(get_text("no_shopping_history", lang))
        else:
            msg = "\n".join(
                f"{h[2]} ➤ {h[1]} (remind: {h[3]})" for h in history
            )
            await query.message.reply_text(msg)
        return

    if data == "tasks":
        tasks = get_tasks(user_id)
        if not tasks:
            await query.message.reply_text(get_text("no_tasks", lang))
        else:
            await query.message.reply_text(
                get_text("your_tasks", lang),
                reply_markup=tasks_menu(tasks)
            )
        return

    if data.startswith("task_done_"):
        task_id = int(data.split("_")[-1])
        set_task_done(user_id, task_id)
        await query.message.reply_text(
            get_text("task_mark_done", lang),
            reply_markup=main_menu()
        )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not validate_session(update, context):
        await update.message.reply_text("⚠️ Your session has expired. Please /start again.")
        return

    text = update.message.text
    user_id = update.effective_user.id
    lang = context.user_data.get("lang", "en")
    mode = context.user_data.get("mode")

    if mode == "ai_chat":
        reply = await ask_ai(text)
        context.user_data["mode"] = None
        await update.message.reply_text(reply, reply_markup=main_menu())
        return

    if mode == "shopping_items":
        context.user_data["shopping_items"] = [x.strip() for x in text.split("\n") if x.strip()]
        await update.message.reply_text(
            get_text("shopping_time_choice", lang),
            reply_markup=shopping_time_menu()
        )
        return

    if mode == "shopping_time":
        add_shopping(user_id, "\n".join(context.user_data.get("shopping_items", [])), text)
        context.user_data["mode"] = None
        await update.message.reply_text(
            get_text("shopping_saved_later", lang).format(remind=text),
            reply_markup=main_menu()
        )
        return

    if text.startswith("/addtask "):
        add_task(user_id, text.replace("/addtask ", "").strip())
        await update.message.reply_text(
            get_text("task_added", lang),
            reply_markup=main_menu()
        )
        return

    await update.message.reply_text(get_text("unknown_input", lang))
