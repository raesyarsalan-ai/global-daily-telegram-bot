from aiogram.types import Message

async def tasks_handler(message: Message):
    await message.answer("Daily tasks feature is active.")
