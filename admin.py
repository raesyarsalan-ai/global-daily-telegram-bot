from aiogram import Router
from aiogram.types import Message
from config import ADMIN_IDS
from payments import approve_payment
from database import db

router = Router()

@router.message(commands=["approve"])
async def approve(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    txid = message.text.split()[1]
    await message.answer("✅ Approved" if await approve_payment(txid) else "❌ Invalid TXID")

@router.message(commands=["stats"])
async def stats(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    u = await db.fetchval("SELECT COUNT(*) FROM users")
    a = await db.fetchval("SELECT COUNT(*) FROM users WHERE subscription_until > NOW()")
    await message.answer(f"Users: {u}\nActive: {a}")
