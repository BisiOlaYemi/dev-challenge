import threading
from datetime import datetime, timedelta, timezone

class RateLimiter:
    """Thread-safe, in-memory rate limiter for external API calls."""
    def __init__(self, max_requests: int, period: timedelta):
        self.max_requests = max_requests
        self.period = period
        self.lock = threading.Lock()
        self.reset()

    def reset(self):
        self.window_start = datetime.now(timezone.utc)
        self.request_count = 0

    def allow(self) -> bool:
        with self.lock:
            now = datetime.now(timezone.utc)
            if now - self.window_start >= self.period:
                self.reset()
            if self.request_count < self.max_requests:
                self.request_count += 1
                return True
            return False 