from database import db

async def register_user(tg_id, username):
    await db.execute(
        "INSERT INTO users (telegram_id, username) VALUES ($1,$2) ON CONFLICT DO NOTHING",
        tg_id, username
    )

async def is_subscribed(tg_id):
    row = await db.fetchrow(
        "SELECT 1 FROM users WHERE telegram_id=$1 AND subscription_until > NOW()", tg_id
    )
    return row is not None

async def set_language(tg_id, lang):
    await db.execute(
        "UPDATE users SET language=$1 WHERE telegram_id=$2", lang, tg_id
    )

async def get_language(tg_id):
    return await db.fetchval(
        "SELECT language FROM users WHERE telegram_id=$1", tg_id
    ) or "en"
