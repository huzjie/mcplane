# Python SDK

```python
from mcplane.sdk.client import McplaneClient

client = McplaneClient("http://127.0.0.1:8090")
print(client.list_tools("echo"))
print(client.call_tool("echo", "echo", {"text": "hello"}))
```

异步客户端：

```python
import asyncio
from mcplane.sdk.async_client import AsyncMcplaneClient

async def main():
    c = AsyncMcplaneClient("http://127.0.0.1:8090")
    print(await c.list_tools("echo"))

asyncio.run(main())
```
