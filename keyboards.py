from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    keyboard = [
        [InlineKeyboardButton("🤖 AI", callback_data="ai")],
    ]
    return InlineKeyboardMarkup(keyboard)


def admin_menu():
    keyboard = [
        [InlineKeyboardButton("👥 Users", callback_data="admin_users")],
    ]
    return InlineKeyboardMarkup(keyboard)
