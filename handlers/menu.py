from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(lang):
    keyboard = [
        [InlineKeyboardButton("✅ Daily Tasks", callback_data="tasks")],
        [InlineKeyboardButton("🛒 Shopping List", callback_data="shopping")],
        [InlineKeyboardButton("📅 Reminders", callback_data="reminders")],
        [InlineKeyboardButton("🤖 AI Assistant", callback_data="ai")],
        [InlineKeyboardButton("⭐ Premium", callback_data="premium")],
    ]
    return InlineKeyboardMarkup(keyboard)
