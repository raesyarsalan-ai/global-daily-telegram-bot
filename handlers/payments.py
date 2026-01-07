from telegram import Update
from telegram.ext import ContextTypes
from database import get_connection


ADMIN_IDS = [123456789]


async def payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "pay_crypto":
        await query.message.reply_text(
            "💳 Send 10 USDT to:\n"
            "`YOUR_WALLET_ADDRESS`\n\n"
            "Then click: I've Paid"
        )

    elif query.data == "paid_manual":
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO payments (telegram_id) VALUES (%s)",
            (user_id,)
        )
        conn.commit()
        cur.close()
        conn.close()

        for admin in ADMIN_IDS:
            await context.bot.send_message(
                admin,
                f"💰 New payment request from {user_id}"
            )

        await query.message.reply_text(
            "✅ Payment submitted.\nWaiting for admin approval."
        )
