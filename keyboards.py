from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from languages import LANGUAGES


def main_menu(lang: str) -> ReplyKeyboardMarkup:
    t = LANGUAGES[lang]

    keyboard = [
        [KeyboardButton(text=t["task"]), KeyboardButton(text=t["shop"])],
        [KeyboardButton(text=t["weather"]), KeyboardButton(text=t["ai"])],
        [KeyboardButton(text=t["buy"]), KeyboardButton(text=t["lang"])],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def task_menu(lang: str) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="➕ Add task")],
        [KeyboardButton(text="📋 My tasks")],
        [KeyboardButton(text="⬅ Back")],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def shopping_menu(lang: str) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="➕ Add item")],
        [KeyboardButton(text="🛒 My list")],
        [KeyboardButton(text="⬅ Back")],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def language_keyboard() -> ReplyKeyboardMarkup:
    keyboard = []
    row = []

    for data in LANGUAGES.values():
        row.append(KeyboardButton(text=data["name"]))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
