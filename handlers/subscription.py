from telegram import Update
from telegram.ext import ContextTypes
from payments.nowpayments import create_invoice
from database import save_payment
from config import SUBSCRIPTION_PRICE_USD


async def buy_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    invoice, order_id = create_invoice(user_id, SUBSCRIPTION_PRICE_USD)
    save_payment(user_id, order_id, SUBSCRIPTION_PRICE_USD)

    await update.callback_query.message.reply_text(
        f"💎 Premium Subscription\n\n"
        f"💰 {SUBSCRIPTION_PRICE_USD}$\n"
        f"🪙 Pay with USDT\n\n"
        f"{invoice['invoice_url']}"
    )
