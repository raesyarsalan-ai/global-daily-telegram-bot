import secrets
import string
from passlib.context import CryptContext
from database import get_user_by_telegram_id, create_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_username():
    """Generate a Telegram-independent username."""
    return "usr_" + secrets.token_hex(4)

def generate_password(length: int = 10) -> str:
    """Generate a random password string."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

def hash_password(password: str) -> str:
    """Hash the user's password securely."""
    return pwd_context.hash(password)

def register_user_if_not_exists(telegram_id):
    """
    Register a user if does not exist.
    Returns:
        dict with username & password (plain) if new,
        None if user already exists.
    """
    user = get_user_by_telegram_id(telegram_id)
    if user:
        return None  # already registered

    username = generate_username()
    password = generate_password()
    password_hash = hash_password(password)

    # Save user in database
    create_user(telegram_id, username, password_hash)

    return {
        "username": username,
        "password": password
    }
