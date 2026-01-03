from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu(lang=None):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Shopping List", callback_data="shop")],
        [InlineKeyboardButton("🤖 Ask AI", callback_data="ai")],
        [InlineKeyboardButton("🌐 Language", callback_data="language")],
    ])
