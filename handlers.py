from aiogram import Router
from aiogram.types import Message, ContentType, ReplyKeyboardMarkup
from users import register_user, is_subscribed, get_language, set_language
from keyboards import main_keyboard
from payments import payment_message, save_payment
from languages import LANGUAGES
from ai import ai_reply
from weather import weather_by_coords

router = Router()

@router.message(commands=["start"])
async def start(message: Message):
    await register_user(message.from_user.id, message.from_user.username)
    lang = await get_language(message.from_user.id)
    await message.answer(LANGUAGES[lang]["welcome"], reply_markup=main_keyboard(lang))

@router.message(content_types=ContentType.LOCATION)
async def location(message: Message):
    w = weather_by_coords(message.location.latitude, message.location.longitude)
    await message.answer(w)

@router.message()
async def main(message: Message):
    uid = message.from_user.id
    lang = await get_language(uid)
    t = LANGUAGES[lang]
    text = message.text

    if text == t["buy"]:
        await message.answer(payment_message())
        return

    if text.startswith("TXID"):
        await save_payment(uid, text.split()[1])
        await message.answer("⏳ Payment received")
        return

    if text == t["lang"]:
        kb = ReplyKeyboardMarkup(
            keyboard=[[v["name"]] for v in LANGUAGES.values()],
            resize_keyboard=True
        )
        await message.answer("🌐 Select language", reply_markup=kb)
        return

    for code, v in LANGUAGES.items():
        if text == v["name"]:
            await set_language(uid, code)
            await message.answer(v["welcome"], reply_markup=main_keyboard(code))
            return

    if not await is_subscribed(uid):
        await message.answer(t["sub"])
        return

    await message.answer(await ai_reply(text))
