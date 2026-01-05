from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import (
    get_all_users,
    set_premium_status,
    get_referral_code,
)

ADMIN_IDS = [123456789]  # آیدی عددی ادمین


# =========================
# ADMIN CHECK
# =========================
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# =========================
# ADMIN MENU
# =========================
def admin_menu():
    keyboard = [
        [InlineKeyboardButton("👥 Users", callback_data="admin_users")],
        [InlineKeyboardButton("⭐ Toggle Premium", callback_data="admin_premium")],
    ]
    return InlineKeyboardMarkup(keyboard)


# =========================
# ADMIN PANEL
# =========================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("⛔ Access denied.")
        return

    await update.message.reply_text(
        "🛠 Admin Panel",
        reply_markup=admin_menu()
    )


# =========================
# ADMIN CALLBACK
# =========================
async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if not is_admin(user_id):
        await query.message.reply_text("⛔ Access denied.")
        return

    data = query.data

    # -------------------------
    # USERS LIST
    # -------------------------
    if data == "admin_users":
        users = get_all_users()
        text = "👥 Users:\n\n"

        for u in users:
            ref = get_referral_code(u["telegram_id"])
            text += (
                f"ID: {u['telegram_id']}\n"
                f"Premium: {u['is_premium']}\n"
                f"Referral: {ref or '-'}\n\n"
            )

        await query.message.reply_text(text)

    # -------------------------
    # TOGGLE PREMIUM (MANUAL)
    # -------------------------
    elif data == "admin_premium":
        await query.message.reply_text(
            "✏️ Send Telegram ID to toggle premium status."
        )
