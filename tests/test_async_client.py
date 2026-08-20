import asyncio

from mcplane.sdk.async_client import AsyncMcplaneClient


def test_async_init():
    c = AsyncMcplaneClient("http://127.0.0.1:8090")
    assert c.base_url == "http://127.0.0.1:8090"
