from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import main_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Welcome to Global Daily Assistant.",
        reply_markup=main_keyboard
    )


@router.message(lambda m: m.text == "Daily Tasks")
async def daily_tasks_handler(message: Message):
    await message.answer("Daily tasks feature is active.")


@router.message(lambda m: m.text == "Shopping List")
async def shopping_handler(message: Message):
    await message.answer("Shopping list feature is active.")


@router.message(lambda m: m.text == "Weather")
async def weather_handler(message: Message):
    await message.answer("Weather feature is active.")


@router.message(lambda m: m.text == "AI Assistant")
async def ai_handler(message: Message):
    await message.answer("AI assistant feature is active.")


@router.message(lambda m: m.text == "Subscription")
async def subscription_handler(message: Message):
    await message.answer("Subscription system is coming soon.")
