import asyncpg
from config import DATABASE_URL

db = None

async def init_db():
    global db
    db = await asyncpg.create_pool(DATABASE_URL)
