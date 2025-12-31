from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from languages import LANGUAGES

def language_keyboard():
    keyboard, row = [], []
    for code, name in LANGUAGES.items():
        row.append(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row: keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📝 Tasks", callback_data="menu_tasks"),
         InlineKeyboardButton("🛒 Shopping", callback_data="menu_shopping")],
        [InlineKeyboardButton("🤖 AI Chat", callback_data="menu_ai")],
        [InlineKeyboardButton("💰 Subscription", callback_data="menu_sub")],
        [InlineKeyboardButton("⚙️ Admin", callback_data="menu_admin")]
    ]
    return InlineKeyboardMarkup(keyboard)
