from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu, shopping_time_menu, tasks_menu
from languages import LANGUAGES
from ai import ask_ai
from storage import (
    init_db,
    add_shopping,
    get_shopping_history,
    add_task,
    get_tasks,
    set_task_done
)

# Initialize database tables when bot starts
init_db()

# Utility to get localized text
def get_text(key: str, lang: str):
    try:
        return LANGUAGES[lang][key]
    except KeyError:
        return LANGUAGES["en"][key]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = context.user_data.get("lang", "en")
    welcome_message = get_text("start", lang)
    await update.message.reply_text(welcome_message, reply_markup=main_menu())

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = context.user_data.get("lang", "en")
    data = query.data

    # Language selection
    if data.startswith("lang_"):
        new_lang = data.split("_")[1]
        context.user_data["lang"] = new_lang
        await query.message.reply_text(get_text("language_changed", new_lang), reply_markup=main_menu())
        return

    # Go to AI Chat mode
    if data == "ai":
        context.user_data["mode"] = "ai_chat"
        await query.message.reply_text(get_text("ask_ai", lang))
        return

    # Shopping flow start
    if data == "shopping":
        context.user_data["mode"] = "shopping_items"
        await query.message.reply_text(get_text("ask_shopping", lang))
        return

    if data == "shop_today":
        items = context.user_data.pop("shopping_items", [])
        add_shopping(user_id, "\n".join(items), "today")
        await query.message.reply_text(get_text("shopping_saved_today", lang), reply_markup=main_menu())
        return

    if data == "shop_later":
        context.user_data["mode"] = "shopping_time"
        await query.message.reply_text(get_text("ask_shopping_time", lang))
        return

    if data == "shop_history":
        history = get_shopping_history(user_id)
        if not history:
            await query.message.reply_text(get_text("no_shopping_history", lang), reply_markup=main_menu())
        else:
            lines = []
            for h in history:
                lines.append(f"{h[2]} ➤ {h[1]} (remind: {h[3]})")
            await query.message.reply_text("\n".join(lines), reply_markup=main_menu())
        return

    # Tasks flow start
    if data == "tasks":
        tasks = get_tasks(user_id)
        if not tasks:
            await query.message.reply_text(get_text("no_tasks", lang), reply_markup=main_menu())
        else:
            await query.message.reply_text(get_text("your_tasks", lang), reply_markup=tasks_menu(tasks))
        return

    if data.startswith("task_done_"):
        task_id = int(data.split("_")[-1])
        set_task_done(user_id, task_id)
        await query.message.reply_text(get_text("task_mark_done", lang), reply_markup=main_menu())
        return

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    lang = context.user_data.get("lang", "en")
    mode = context.user_data.get("mode")

    # AI Chat
    if mode == "ai_chat":
        reply = await ask_ai(text)
        await update.message.reply_text(reply, reply_markup=main_menu())
        context.user_data["mode"] = None
        return

    # Shopping list text
    if mode == "shopping_items":
        items = [x.strip() for x in text.split("\n") if x.strip()]
        context.user_data["shopping_items"] = items
        await update.message.reply_text(get_text("shopping_time_choice", lang), reply_markup=shopping_time_menu())
        return

    # Shopping time
    if mode == "shopping_time":
        add_shopping(user_id, "\n".join(context.user_data.get("shopping_items", [])), text)
        await update.message.reply_text(get_text("shopping_saved_later", lang).format(remind=text), reply_markup=main_menu())
        context.user_data["mode"] = None
        return

    # Add a new task
    if text.startswith("/addtask "):
        task_text = text.replace("/addtask ", "").strip()
        add_task(user_id, task_text)
        await update.message.reply_text(get_text("task_added", lang), reply_markup=main_menu())
        return

    await update.message.reply_text(get_text("unknown_input", lang), reply_markup=main_menu())
