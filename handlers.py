from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from database import add_task, get_tasks, mark_task_done
from languages import LANGUAGES

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # گرفتن زبان کاربر، پیشفرض انگلیسی
    lang = context.user_data.get("lang", "en")
    context.user_data["lang"] = lang
    text = f"{LANGUAGES[lang]['welcome']}"

    keyboard = [
        [InlineKeyboardButton(LANGUAGES[lang]['task'], callback_data="menu_task")],
        [InlineKeyboardButton(LANGUAGES[lang]['shop'], callback_data="menu_shop")],
        [InlineKeyboardButton(LANGUAGES[lang]['weather'], callback_data="menu_weather")],
        [InlineKeyboardButton(LANGUAGES[lang]['ai'], callback_data="menu_ai")],
        [InlineKeyboardButton(LANGUAGES[lang]['buy'], callback_data="menu_subscription")],
        [InlineKeyboardButton(LANGUAGES[lang]['lang'], callback_data="menu_lang")],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang_buttons = [[InlineKeyboardButton(LANGUAGES[l]["name"], callback_data=f"setlang_{l}")] for l in LANGUAGES]
    await query.edit_message_text("🌐 Select language / انتخاب زبان:", reply_markup=InlineKeyboardMarkup(lang_buttons))


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang_code = query.data.split("_")[1]
    context.user_data["lang"] = lang_code
    await query.edit_message_text(f"✅ Language set to {LANGUAGES[lang_code]['name']}")
    # برگشت به منوی اصلی
    await start_handler(update, context)


async def menu_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    lang = context.user_data.get("lang", "en")

    if query.data == "menu_task":
        tasks = get_tasks(user_id)
        if not tasks:
            await query.edit_message_text("📝 You have no tasks.")
        else:
            msg = "📝 Your tasks:\n\n"
            for tid, text_task, done in tasks:
                status = "✅" if done else "⏳"
                msg += f"{tid}. {status} {text_task}\n"
            await query.edit_message_text(msg)
    elif query.data == "menu_shop":
        await query.edit_message_text("🛒 Shopping list feature coming soon")
    elif query.data == "menu_weather":
        await query.edit_message_text("🌤 Weather feature coming soon")
    elif query.data == "menu_ai":
        await query.edit_message_text("🤖 AI chat feature coming soon")
    elif query.data == "menu_subscription":
        await query.edit_message_text(f"{LANGUAGES[lang]['sub']}")
    elif query.data == "menu_lang":
        await language_handler(update, context)


# Task commands
async def add_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /addtask Buy milk")
        return
    user_id = update.effective_user.id
    text = " ".join(context.args)
    add_task(user_id, text)
    await update.message.reply_text("✅ Task added")


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
