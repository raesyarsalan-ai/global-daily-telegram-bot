from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from languages import LANGUAGES

def main_keyboard(lang):
    t = LANGUAGES[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["task"]), KeyboardButton(text=t["shop"])],
            [KeyboardButton(text=t["weather"]), KeyboardButton(text=t["ai"])],
            [KeyboardButton(text=t["buy"]), KeyboardButton(text=t["lang"])]
        ],
        resize_keyboard=True
    )
