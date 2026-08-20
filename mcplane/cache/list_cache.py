"""Cache for ``tools/list`` results with cacheScope semantics.

The stateless spec adds ``ttlMs`` and ``cacheScope`` hints to list responses so
clients can cache aggressively and save round-trips. This cache implements that
contract server-side for gateway-side caching.
"""

import time

from .ttl_cache import TtlCache


class ListResultCache:
    def __init__(self, default_ttl_ms: int = 60000, max_entries: int = 4096):
        self._cache = TtlCache(default_ttl_s=default_ttl_ms / 1000.0,
                               max_entries=max_entries)
        self.default_ttl_ms = default_ttl_ms

    def cache_key(self, server_name: str, method: str, scope: str = "server") -> str:
        if scope == "server":
            return "%s::%s" % (server_name, method)
        return "%s::%s::global" % (server_name, method)

    def get(self, server_name: str, method: str, scope: str = "server"):
        return self._cache.get(self.cache_key(server_name, method, scope))

    def set(self, server_name: str, method: str, value, ttl_ms: int = None,
            scope: str = "server"):
        ttl_s = (ttl_ms if ttl_ms is not None else self.default_ttl_ms) / 1000.0
        self._cache.set(self.cache_key(server_name, method, scope), value, ttl_s=ttl_s)

    def __len__(self):
        return len(self._cache)
