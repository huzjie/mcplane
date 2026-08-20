"""Demo: use the Python SDK against a running mcplane gateway."""

import sys

from mcplane.sdk.client import McplaneClient


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8090"
    client = McplaneClient(base)

    print("== list_tools ==")
    result = client.list_tools("echo")
    print(result)

    print("== call_tool(echo) ==")
    result = client.call_tool("echo", "echo", {"text": "hello stateless MCP"})
    print(result)

    print("== call_tool(calculator) ==")
    result = client.call_tool("echo", "calculator", {"expression": "1 + 2 * 3"})
    print(result)


if __name__ == "__main__":
    main()
