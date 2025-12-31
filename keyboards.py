from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from languages import LANGUAGES

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Add Task", callback_data="task")],
        [InlineKeyboardButton("🤖 Ask AI", callback_data="ai")],
        [InlineKeyboardButton("🌐 Language", callback_data="language")]
    ])

def language_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(v["name"], callback_data=f"lang_{k}")]
        for k, v in LANGUAGES.items()
    ])
