import hashlib

def generate_device_fingerprint(update):
    raw = f"{update.effective_user.id}-{update.effective_user.username}"
    return hashlib.sha256(raw.encode()).hexdigest()
