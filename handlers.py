from telegram import Update
from telegram.ext import ContextTypes

from keyboards import main_menu, language_menu
from languages import get_text

USER_LANGUAGE = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    USER_LANGUAGE[user_id] = "en"

    await update.message.reply_text(
        get_text("en", "welcome"),
        reply_markup=main_menu()
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    lang = USER_LANGUAGE.get(user_id, "en")

    if text == "📝 Daily Tasks":
        await update.message.reply_text(get_text(lang, "tasks"))

    elif text == "🛒 Shopping List":
        await update.message.reply_text(get_text(lang, "shopping"))

    elif text == "🌤 Weather":
        await update.message.reply_text(get_text(lang, "weather"))

    elif text == "🌍 Language":
        await update.message.reply_text(
            get_text(lang, "choose_language"),
            reply_markup=language_menu()
        )

    elif text == "🇺🇸 English":
        USER_LANGUAGE[user_id] = "en"
        await update.message.reply_text(
            "Language set to English",
            reply_markup=main_menu()
        )

    elif text == "🇮🇷 Persian":
        USER_LANGUAGE[user_id] = "fa"
        await update.message.reply_text(
            "Language set to Persian",
            reply_markup=main_menu()
        )

    elif text == "⬅️ Back":
        await update.message.reply_text(
            get_text(lang, "welcome"),
            reply_markup=main_menu()
        )

    elif text == "ℹ️ About":
        await update.message.reply_text(get_text(lang, "about"))

    else:
        await update.message.reply_text(
            "Please use the menu buttons.",
            reply_markup=main_menu()
        )
