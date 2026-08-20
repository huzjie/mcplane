import json
import os
import tempfile

from mcplane.registry.server_registry import ServerRegistry
from mcplane.registry.discovery import discover_servers


def test_discover_from_json():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"echo": {"url": "http://127.0.0.1:8100/mcp"}}, f)
        path = f.name
    try:
        reg = ServerRegistry()
        count = discover_servers(reg, [path])
        assert count == 1
        assert reg.get("echo").url == "http://127.0.0.1:8100/mcp"
    finally:
        os.unlink(path)


def test_discover_missing_file_skipped():
    reg = ServerRegistry()
    count = discover_servers(reg, ["/no/such/file.json"])
    assert count == 0
