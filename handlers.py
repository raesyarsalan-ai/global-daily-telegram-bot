from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from languages import LANGUAGES
from keyboards import main_menu, language_keyboard
from database import get_language, set_language

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    lang = await get_language(user_id)

    if not lang:
        await message.answer(
            "Please choose your language 🌐",
            reply_markup=language_keyboard()
        )
        return

    await message.answer(
        LANGUAGES[lang]["welcome"],
        reply_markup=main_menu(lang)
    )


@router.message(lambda m: m.text in [v["name"] for v in LANGUAGES.values()])
async def language_selected(message: Message):
    user_id = message.from_user.id

    for code, data in LANGUAGES.items():
        if message.text == data["name"]:
            await set_language(user_id, code)
            await message.answer(
                data["welcome"],
                reply_markup=main_menu(code)
            )
            return


@router.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text
    lang = await get_language(user_id)

    if not lang:
        await start_handler(message)
        return

    t = LANGUAGES[lang]

    if text == t["task"]:
        await message.answer("Task system ready.")

    elif text == t["shop"]:
        await message.answer("Shopping system ready.")

    elif text == t["weather"]:
        await message.answer("Weather system ready.")

    elif text == t["ai"]:
        await message.answer("AI Chat coming soon.")

    elif text == t["buy"]:
        await message.answer(t["sub"])

    elif text == t["lang"]:
        await message.answer(
            "Choose language 🌐",
            reply_markup=language_keyboard()
        )

    else:
        await message.answer(
            t["welcome"],
            reply_markup=main_menu(lang)
        )
async def add_task_handler(update, context):
    ...
