from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# =========================
# MAIN MENU
# =========================
def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("✅ Daily Check-in", callback_data="daily_checkin")
        ],
        [
            InlineKeyboardButton("🧠 Mood Today", callback_data="mood_menu"),
            InlineKeyboardButton("👤 Profile", callback_data="profile")
        ],
        [
            InlineKeyboardButton("🔗 Referral", callback_data="referral")
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# =========================
# MOOD MENU
# =========================
def mood_menu():
    keyboard = [
        [
            InlineKeyboardButton("😊 Happy", callback_data="mood_happy"),
            InlineKeyboardButton("😐 Neutral", callback_data="mood_neutral"),
            InlineKeyboardButton("😔 Sad", callback_data="mood_sad"),
        ],
        [
            InlineKeyboardButton("😡 Angry", callbac
