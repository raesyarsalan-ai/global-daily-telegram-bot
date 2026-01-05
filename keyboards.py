from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(is_admin=False):
    keyboard = [
        [InlineKeyboardButton("🤖 Ask AI", callback_data="ai")],
        [InlineKeyboardButton("🛒 Shopping List", callback_data="shopping")],
        [InlineKeyboardButton("📝 Tasks", callback_data="tasks")],
        [InlineKeyboardButton("🌐 Language", callback_data="language")],
    ]

    if is_admin:
        keyboard.append(
            [InlineKeyboardButton("🛠 Admin Panel", callback_data="admin_panel")]
        )

    return InlineKeyboardMarkup(keyboard)


def admin_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 View Users", callback_data="admin_users")],
        [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_menu")]
    ])
