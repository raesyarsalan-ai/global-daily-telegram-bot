from database import db
from config import USDT_WALLET, SUB_PRICE

def payment_message():
    return (
        f"💳 {SUB_PRICE} USDT / 30 days\n\n"
        f"Wallet (TRC20):\n{USDT_WALLET}\n\n"
        f"Send:\nTXID <hash>"
    )

async def save_payment(tg_id, txid):
    await db.execute(
        "INSERT INTO payments (txid, telegram_id) VALUES ($1,$2) ON CONFLICT DO NOTHING",
        txid, tg_id
    )

async def approve_payment(txid):
    user = await db.fetchrow(
        "SELECT telegram_id FROM payments WHERE txid=$1 AND status='pending'", txid
    )
    if not user:
        return False

    await db.execute("UPDATE payments SET status='approved' WHERE txid=$1", txid)
    await db.execute(
        "UPDATE users SET is_active=TRUE, subscription_until=NOW()+INTERVAL '30 days' WHERE telegram_id=$1",
        user["telegram_id"]
    )
    return True
