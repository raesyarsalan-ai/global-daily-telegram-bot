from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu
from middlewares import user_guard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await user_guard(update, context):
        return

    await update.message.reply_text(
        "👋 Welcome to Global Daily Assistant Bot",
        reply_markup=main_menu()
    )
