from telegram import ReplyKeyboardMarkup
from languages import LANGUAGES, get_text


def language_keyboard():
    keyboard = [[data["name"]] for data in LANGUAGES.values()]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def main_menu(lang: str):
    keyboard = [
        [get_text(lang, "task"), get_text(lang, "shop")],
        [get_text(lang, "weather"), get_text(lang, "ai")],
        [get_text(lang, "lang"), get_text(lang, "buy")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
