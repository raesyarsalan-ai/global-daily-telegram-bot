import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DB_NAME = "daily_helper.db"
AI_MODEL = "gpt-4o-mini"
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", None)

# PostgreSQL database settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "global_daily_bot")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Make sure BOT_TOKEN is provided
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables!")

