"""End-to-end: gateway -> mock server over real HTTP (stdlib)."""

import json
import threading
import time
import urllib.request

from mcplane.config import load_config
from mcplane.server.app import Gateway
from mcplane.server.mock_server import MockMcpServer


def test_gateway_handle_echo():
    # Start a mock MCP server on an ephemeral port.
    mock = MockMcpServer(port=0)
    mock.port = 0
    # Use a fixed high port to avoid collisions in CI.
    import socket
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    mock.port = port
    httpd = mock.start()
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()

    config = load_config()
    config["registry"]["discovery_paths"] = []
    gw = Gateway(config)
    from mcplane.registry.server_registry import ServerRecord
    gw.registry.register(ServerRecord(name="echo", url="http://127.0.0.1:%d/mcp" % port))

    try:
        body = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                "params": {"name": "echo", "arguments": {"text": "e2e"}}}
        result = gw.handle(body, {"mcp-name": "echo", "mcp-method": "tools/call"})
        assert result["result"]["content"][0]["text"] == "e2e"
    finally:
        httpd.shutdown()
        httpd.server_close()
