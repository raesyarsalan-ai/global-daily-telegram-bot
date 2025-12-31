from aiogram.types import Message

async def shopping_handler(message: Message):
    await message.answer("Shopping list feature is active.")
