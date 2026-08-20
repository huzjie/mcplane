"""Demo: use the async SDK against a running mcplane gateway."""

import asyncio

from mcplane.sdk.async_client import AsyncMcplaneClient


async def main():
    client = AsyncMcplaneClient("http://127.0.0.1:8090")
    tools = await client.list_tools("echo")
    print(tools)
    result = await client.call_tool("echo", "echo", {"text": "async hello"})
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
