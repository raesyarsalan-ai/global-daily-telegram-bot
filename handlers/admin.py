from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta

from database import get_connection
from database.subscription import set_subscription

ADMIN_IDS = [123456789]


async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, telegram_id FROM payments
        WHERE status='pending'
    """)
    rows = cur.fetchall()

    if not rows:
        await update.message.reply_text("No pending payments.")
        return

    for pid, user_id in rows:
        await update.message.reply_text(
            f"Approve payment {pid} for user {user_id}?\n"
            f"/approve_{pid}"
        )

    cur.close()
    conn.close()


async def approve_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    pid = int(update.message.text.split("_")[1])

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT telegram_id FROM payments WHERE id=%s",
        (pid,)
    )
    user_id = cur.fetchone()[0]

    expires = datetime.utcnow() + timedelta(days=30)
    set_subscription(user_id, expires)

    cur.execute(
        "UPDATE payments SET status='approved' WHERE id=%s",
        (pid,)
    )
    conn.commit()

    cur.close()
    conn.close()

    await update.message.reply_text("✅ Subscription activated.")
