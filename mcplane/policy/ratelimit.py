"""Thread-safe token-bucket rate limiter (stdlib only)."""

import threading
import time

from ..errors import RateLimitError


class TokenBucket:
    def __init__(self, rate: float, burst: int):
        self.rate = rate
        self.burst = burst
        self.tokens = float(burst)
        self.updated = time.monotonic()
        self._lock = threading.Lock()

    def consume(self, amount: int = 1) -> bool:
        with self._lock:
            now = time.monotonic()
            elapsed = now - self.updated
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
            self.updated = now
            if self.tokens >= amount:
                self.tokens -= amount
                return True
            return False


class RateLimiter:
    def __init__(self, requests_per_second: float = 100, burst: int = 200):
        self._buckets = {}
        self._rate = requests_per_second
        self._burst = burst
        self._lock = threading.Lock()

    def _bucket(self, key: str) -> TokenBucket:
        with self._lock:
            if key not in self._buckets:
                self._buckets[key] = TokenBucket(self._rate, self._burst)
            return self._buckets[key]

    def allow(self, key: str, amount: int = 1) -> bool:
        return self._bucket(key).consume(amount)

    def guard(self, key: str, amount: int = 1):
        if not self.allow(key, amount):
            raise RateLimitError("rate limit exceeded for %s" % key)
