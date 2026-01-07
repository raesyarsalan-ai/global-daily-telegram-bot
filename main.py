from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN
from database import init_db
from handlers.start import start
from handlers.premium import premium_handler

def main():
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("premium", premium_handler))

    print("🤖 Bot running (Production)")
    app.run_polling()

if __name__ == "__main__":
    main()
