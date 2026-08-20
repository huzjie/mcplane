"""Thread-safe TTL cache (stdlib only)."""

import threading
import time


class TtlCache:
    def __init__(self, default_ttl_s: float = 60.0, max_entries: int = 4096):
        self.default_ttl_s = default_ttl_s
        self.max_entries = max_entries
        self._store = {}
        self._lock = threading.Lock()

    def get(self, key: str):
        with self._lock:
            item = self._store.get(key)
            if not item:
                return None
            value, expiry = item
            if expiry < time.monotonic():
                self._store.pop(key, None)
                return None
            return value

    def set(self, key: str, value, ttl_s: float = None):
        ttl = ttl_s if ttl_s is not None else self.default_ttl_s
        expiry = time.monotonic() + ttl
        with self._lock:
            if len(self._store) >= self.max_entries and key not in self._store:
                oldest = min(self._store.items(), key=lambda kv: kv[1][1])
                self._store.pop(oldest[0], None)
            self._store[key] = (value, expiry)

    def clear(self):
        with self._lock:
            self._store.clear()

    def __len__(self):
        with self._lock:
            return len(self._store)
