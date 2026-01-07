from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 AI Assistant", callback_data="ai")],
        [InlineKeyboardButton("🛒 Shopping List", callback_data="shopping")],
        [InlineKeyboardButton("⏰ Reminders", callback_data="reminders")],
        [InlineKeyboardButton("🌤 Weather", callback_data="weather")],
    ])
