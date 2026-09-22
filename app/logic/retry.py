import time

def retry_with_backoff(fn, max_retries: int = 3):
    attempt = 0
    while attempt < max_retries:
        try:
            return fn()
        except Exception:
            # BUG: attempt is never incremented — infinite loop on failure
            time.sleep(2 ** attempt)
    raise RuntimeError("Max retries exceeded")
