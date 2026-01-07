from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(lang: str):
    keyboard = [
        [InlineKeyboardButton("✅ Tasks", callback_data="tasks")],
        [InlineKeyboardButton("⏰ Add Reminder", callback_data="add_reminder")],
        [InlineKeyboardButton("🛒 Shopping List", callback_data="shopping")],
        [InlineKeyboardButton("🤖 AI Assistant", callback_data="ai")],
        [InlineKeyboardButton("⭐ Premium", callback_data="premium")],
    ]
    return InlineKeyboardMarkup(keyboard)
