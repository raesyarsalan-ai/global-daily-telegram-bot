import os
from urllib.parse import urlparse


# =========================
# BOT & AI
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# =========================
# DATABASE (Railway Compatible)
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    result = urlparse(DATABASE_URL)

    DB_HOST = result.hostname
    DB_PORT = result.port
    DB_NAME = result.path.lstrip("/")
    DB_USER = result.username
    DB_PASSWORD = result.password
else:
    # Local / Manual fallback
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")


# =========================
# WEATHER
# =========================
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# =========================
# CRYPTO PAYMENT (CryptoBot)
# =========================
CRYPTO_API_KEY = os.getenv("CRYPTO_API_KEY")


# =========================
# PROJECT SETTINGS
# =========================
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = [
    "en", "fa", "ar", "de", "fr", "es", "it",
    "ru", "tr", "pt", "nl", "pl", "uk", "hi"
]

PREMIUM_SUBSCRIPTION_PRICE = 5.0  # USDT
