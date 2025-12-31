from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import main_keyboard
from database import add_user

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await add_user(message.from_user.id)

    await message.answer(
        "Welcome to Global Daily Assistant.",
        reply_markup=main_keyboard
    )
