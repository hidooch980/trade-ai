import time
from collections import defaultdict
from threading import Lock

class LoginRateLimiter:
    def __init__(self, max_attempts: int = 5, window_seconds: int = 300, block_seconds: int = 900):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self.block_seconds = block_seconds
        self._attempts = defaultdict(list)
        self._blocked = {}
        self._lock = Lock()

    def _cleanup(self, key: str, now: float):
        self._attempts[key] = [
            ts for ts in self._attempts[key]
            if now - ts < self.window_seconds
        ]

    def is_blocked(self, key: str) -> bool:
        now = time.time()
        with self._lock:
            blocked_until = self._blocked.get(key)
            if blocked_until and blocked_until > now:
                return True
            if blocked_until:
                self._blocked.pop(key, None)
            self._cleanup(key, now)
            return False

    def register_failure(self, key: str) -> None:
        now = time.time()
        with self._lock:
            self._cleanup(key, now)
            self._attempts[key].append(now)
            if len(self._attempts[key]) >= self.max_attempts:
                self._blocked[key] = now + self.block_seconds
                self._attempts[key].clear()

    def register_success(self, key: str) -> None:
        with self._lock:
            self._attempts.pop(key, None)
            self._blocked.pop(key, None)

login_rate_limiter = LoginRateLimiter(
    max_attempts=5,
    window_seconds=300,
    block_seconds=900,
)
