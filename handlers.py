from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import add_task, get_tasks, mark_task_done, set_language

# Start handler با کیبورد 14 زبان
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="lang_en"),
            InlineKeyboardButton("فارسی", callback_data="lang_fa"),
            InlineKeyboardButton("Español", callback_data="lang_es"),
            InlineKeyboardButton("Français", callback_data="lang_fr"),
        ],
        [
            InlineKeyboardButton("Deutsch", callback_data="lang_de"),
            InlineKeyboardButton("中文", callback_data="lang_zh"),
            InlineKeyboardButton("日本語", callback_data="lang_ja"),
            InlineKeyboardButton("Русский", callback_data="lang_ru"),
        ],
        [
            InlineKeyboardButton("العربية", callback_data="lang_ar"),
            InlineKeyboardButton("हिन्दी", callback_data="lang_hi"),
            InlineKeyboardButton("Português", callback_data="lang_pt"),
            InlineKeyboardButton("Italiano", callback_data="lang_it"),
        ],
        [
            InlineKeyboardButton("Türkçe", callback_data="lang_tr"),
            InlineKeyboardButton("한국어", callback_data="lang_ko"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome!\nPlease select your language:",
        reply_markup=reply_markup
    )


# هندلر انتخاب زبان از کیبورد
async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang_code = query.data.split("_")[1]  # استخراج کد زبان
    user_id = query.from_user.id
    set_language(user_id, lang_code)
    await query.edit_message_text(f"Language set to {lang_code}")


async def add_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /addtask Buy milk")
        return

    user_id = update.effective_user.id
    text = " ".join(context.args)

    add_task(user_id, text)
    await update.message.reply_text("✅ Task added")


async def list_tasks_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = get_tasks(user_id)

    if not tasks:
        await update.message.reply_text("📝 You have no tasks.")
        return

    message = "📝 Your tasks:\n\n"
    for task_id, text, is_done in tasks:
        status = "✅" if is_done else "⏳"
        message += f"{task_id}. {status} {text}\n"

    await update.message.reply_text(message)


async def done_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /donetask 1")
        return

    user_id = update.effective_user.id

    try:
        task_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Task id must be a number.")
        return

    mark_task_done(task_id, user_id)
    await update.message.reply_text("✅ Task marked as done")
