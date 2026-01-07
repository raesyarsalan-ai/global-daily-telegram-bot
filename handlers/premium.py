from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from payments.crypto import create_invoice


async def premium_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    invoice = create_invoice(update.effective_user.id)

    if not invoice:
        await update.message.reply_text("❌ Payment service unavailable.")
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Pay Now", url=invoice["pay_url"])]
    ])

    await update.message.reply_text(
        "⭐ Premium – 10 USDT / month",
        reply_markup=keyboard
    )
