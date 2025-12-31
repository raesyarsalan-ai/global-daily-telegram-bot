from telegram import Update
from telegram.ext import ContextTypes
from languages import LANGUAGES, get_text
from keyboards import main_menu, language_keyboard

USER_LANGUAGE = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in USER_LANGUAGE:
        await update.message.reply_text(
            "Please choose your language 🌐",
            reply_markup=language_keyboard()
        )
        return

    lang = USER_LANGUAGE[user_id]
    await update.message.reply_text(
        get_text(lang, "welcome"),
        reply_markup=main_menu(lang)
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    # Language selection
    for code, data in LANGUAGES.items():
        if text == data["name"]:
            USER_LANGUAGE[user_id] = code
            await update.message.reply_text(
                data["welcome"],
                reply_markup=main_menu(code)
            )
            return

    lang = USER_LANGUAGE.get(user_id)
    if not lang:
        await start(update, context)
        return

    if text == get_text(lang, "task"):
        await update.message.reply_text("Task system ready.")

    elif text == get_text(lang, "shop"):
        await update.message.reply_text("Shopping system ready.")

    elif text == get_text(lang, "weather"):
        await update.message.reply_text("Weather system ready.")

    elif text == get_text(lang, "ai"):
        await update.message.reply_text("AI Chat coming soon.")

    elif text == get_text(lang, "buy"):
        await update.message.reply_text(get_text(lang, "sub"))

    elif text == get_text(lang, "lang"):
        await update.message.reply_text(
            "Choose language 🌐",
            reply_markup=language_keyboard()
        )

    else:
        await update.message.reply_text(
            get_text(lang, "welcome"),
            reply_markup=main_menu(lang)
        )
