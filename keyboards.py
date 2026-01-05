def shopping_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ New Shopping List", callback_data="shop_new")],
        [InlineKeyboardButton("📜 History", callback_data="shop_history")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_menu")],
    ])


def shopping_time_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🕒 Today", callback_data="shop_today")],
        [InlineKeyboardButton("📅 Set Time", callback_data="shop_later")],
    ])
