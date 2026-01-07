from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import get_or_create_user
from languages import LANGUAGES


def language_keyboard():
    keyboard = []
    row = []
    for code, data in LANGUAGES.items():
        row.append(
            InlineKeyboardButton(data["name"], callback_data=f"lang_{code}")
        )
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_or_create_user(user.id, user.username)

    await update.message.reply_text(
        "🌍 Please choose your language:",
        reply_markup=language_keyboard()
    )
