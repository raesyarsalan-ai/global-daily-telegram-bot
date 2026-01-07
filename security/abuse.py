import time

REQUEST_LIMIT = 8
WINDOW = 60

_cache = {}

def check_rate_limit(user_id):
    now = time.time()
    window = _cache.get(user_id, [])
    window = [t for t in window if now - t < WINDOW]

    if len(window) >= REQUEST_LIMIT:
        return False

    window.append(now)
    _cache[user_id] = window
    return True
