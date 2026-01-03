from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 Ask AI", callback_data="ask_ai")],
        [InlineKeyboardButton("🛒 Shopping List", callback_data="shopping")],
        [InlineKeyboardButton("📝 Tasks", callback_data="task")],
    ])

def shopping_time_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🕒 Today", callback_data="shop_today")],
        [InlineKeyboardButton("📅 Another time", callback_data="shop_later")],
    ])
