from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from languages import TEXTS

def t(key, lang):
    return TEXTS.get(key, {}).get(lang) or TEXTS[key]["en"]

def main_menu(lang="en"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Add Task", callback_data="task")],
        [InlineKeyboardButton("🛒 Shopping List", callback_data="shopping")],
        [InlineKeyboardButton("🤖 Ask AI", callback_data="ai")],
        [InlineKeyboardButton("🌐 Language", callback_data="language")],
    ])

def language_menu():
    from languages import LANGUAGES
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(v["name"], callback_data=f"lang_{k}")]
        for k, v in LANGUAGES.items()
    ])
