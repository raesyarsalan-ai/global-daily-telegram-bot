from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Daily Tasks")],
        [KeyboardButton(text="Shopping List")],
        [KeyboardButton(text="Weather")],
        [KeyboardButton(text="AI Assistant")],
        [KeyboardButton(text="Subscription")]
    ],
    resize_keyboard=True
)
