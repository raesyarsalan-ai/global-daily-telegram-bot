from telegram import Update
from telegram.ext import ContextTypes
from keyboards import language_keyboard, main_menu_keyboard
from database import (
    set_user_language, get_user_language,
    add_task, get_tasks, mark_task_done,
    add_shopping, get_shopping, mark_shopping_done
)

# START
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Choose language:", reply_markup=language_keyboard())

# LANGUAGE CALLBACK
async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    code = query.data.split("_")[1]
    uid = query.from_user.id
    set_user_language(uid, code)
    await query.edit_message_text(f"Language set to {code}", reply_markup=main_menu_keyboard())

# MAIN MENU
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_tasks":
        await query.edit_message_text("Manage tasks:\nUse /addtask, /tasks, /donetask")
    elif data == "menu_shopping":
        await query.edit_message_text("Shopping list:\nUse /addshopping, /shopping, /doneshopping")
    elif data == "menu_ai":
        await query.edit_message_text("Chat with AI\nUse /ai <text>")
    elif data == "menu_sub":
        await query.edit_message_text("Subscription:\nUse /subscribe")
    elif data == "menu_admin":
        await query.edit_message_text("Admin Panel")

# TASKS
async def add_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /addtask Buy milk")
        return
    add_task(update.effective_user.id, " ".join(context.args))
    await update.message.reply_text("Task added!")

async def list_tasks_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_tasks(update.effective_user.id)
    msg = "Your tasks:\n"
    for i, t, d in tasks: msg += f"{i}. {'✔' if d else '❌'} {t}\n"
    await update.message.reply_text(msg)

async def done_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mark_task_done(int(context.args[0]), update.effective_user.id)
        await update.message.reply_text("Task done!")
    except:
        await update.message.reply_text("Invalid usage")

# SHOPPING
async def add_shopping_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /addshopping item")
        return
    add_shopping(update.effective_user.id, " ".join(context.args))
    await update.message.reply_text("Item added!")

async def list_shopping_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = get_shopping(update.effective_user.id)
    msg = "Shopping list:\n"
    for i, t, d in items: msg += f"{i}. {'✔' if d else '❌'} {t}\n"
    await update.message.reply_text(msg)

async def done_shopping_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mark_shopping_done(int(context.args[0]), update.effective_user.id)
        await update.message.reply_text("Item done!")
    except:
        await update.message.reply_text("Invalid usage")

