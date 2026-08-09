import time
from collections import defaultdict
from threading import Lock


class AuthRateLimiter:
    def __init__(self):
        self._lock = Lock()
        self._attempts = defaultdict(list)

    def check(
        self,
        key: str,
        limit: int,
        window_seconds: int,
    ) -> bool:
        now = time.time()

        with self._lock:
            attempts = self._attempts[key]

            self._attempts[key] = [
                timestamp
                for timestamp in attempts
                if now - timestamp < window_seconds
            ]

            if len(self._attempts[key]) >= limit:
                return False

            self._attempts[key].append(now)
            return True

    def clear(self, key: str) -> None:
        with self._lock:
            self._attempts.pop(key, None)


auth_rate_limiter = AuthRateLimiter()
