import os

# =========================
# BOT & AI
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")

# =========================
# DATABASE (PostgreSQL)
# =========================
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "global_daily_bot")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# =========================
# ADMIN
# =========================
ADMIN_IDS = list(
    map(int, os.getenv("ADMIN_IDS", "123456789").split(","))
)

# =========================
# PAYMENTS
# =========================
CRYPTO_API_KEY = os.getenv("CRYPTO_API_KEY")

# =========================
# VALIDATION
# =========================
if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN is not set")
