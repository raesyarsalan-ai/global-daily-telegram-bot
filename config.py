import os

BOT_TOKEN = os.getenv("BOT_TOKEN", None)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

AI_MODEL = "gpt-4o-mini"

# PostgreSQL database settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "global_daily_bot")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Admin Telegram IDs
ADMIN_IDS = [
    123456789  # ← آیدی عددی تلگرام خودت
]

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables!")
