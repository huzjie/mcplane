import time

from mcplane.cache.ttl_cache import TtlCache
from mcplane.cache.list_cache import ListResultCache


def test_ttl_get_set():
    c = TtlCache(default_ttl_s=60)
    c.set("k", "v")
    assert c.get("k") == "v"


def test_ttl_expiry():
    c = TtlCache(default_ttl_s=0.01)
    c.set("k", "v")
    time.sleep(0.03)
    assert c.get("k") is None


def test_list_cache_key():
    c = ListResultCache()
    c.set("echo", "tools/list", {"tools": []}, ttl_ms=1000)
    assert c.get("echo", "tools/list") == {"tools": []}
