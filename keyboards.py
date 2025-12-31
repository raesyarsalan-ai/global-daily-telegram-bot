from telegram import ReplyKeyboardMarkup

def main_menu():
    keyboard = [
        ["📝 Daily Tasks", "🛒 Shopping List"],
        ["🌤 Weather", "🌍 Language"],
        ["ℹ️ About"]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


def language_menu():
    keyboard = [
        ["🇺🇸 English", "🇮🇷 Persian"],
        ["⬅️ Back"]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
