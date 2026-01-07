from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def premium_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💳 Pay with Crypto", callback_data="pay_crypto")],
        [InlineKeyboardButton("📨 I've Paid", callback_data="paid_manual")]
    ]

    await update.message.reply_text(
        "⭐ Premium Plan:\n"
        "- Unlimited AI\n"
        "- Unlimited reminders\n"
        "- Smart scheduling\n\n"
        "Price: 10 USDT / month",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
