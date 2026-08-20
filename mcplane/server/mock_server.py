"""A self-contained mock MCP server for local testing.

Implements a tiny JSON-RPC-over-HTTP MCP server with a couple of sample tools
(echo, calculator) using only the standard library, so end-to-end tests run
with zero external dependencies.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict


class MockMcpServer:
    """Standalone mock MCP server exposing ``echo`` and ``calculator`` tools."""

    TOOLS = [
        {"name": "echo", "description": "Echo back the input text.",
         "inputSchema": {"type": "object",
                         "properties": {"text": {"type": "string"}}}},
        {"name": "calculator", "description": "Evaluate a simple arithmetic expression.",
         "inputSchema": {"type": "object",
                         "properties": {"expression": {"type": "string"}}}},
    ]

    def __init__(self, port: int = 8100):
        self.port = port
        self._httpd = None

    def handle(self, body: Dict) -> Dict:
        method = body.get("method")
        params = body.get("params") or {}
        if method == "tools/list":
            return {"tools": self.TOOLS}
        if method == "tools/call":
            return self._call(params)
        if method == "ping":
            return {}
        if method == "initialize":
            return {"protocolVersion": "2026-07-28",
                    "capabilities": {"tools": {}}}
        return {"error": {"code": -32601, "message": "method not found"}}

    def _call(self, params):
        name = params.get("name")
        args = params.get("arguments") or {}
        if name == "echo":
            text = args.get("text", "")
            return {"content": [{"type": "text", "text": text}]}
        if name == "calculator":
            expr = args.get("expression", "")
            try:
                # Restricted eval over a small safe namespace.
                value = eval(expr, {"__builtins__": {}}, {})  # noqa: S307
            except Exception as exc:
                return {"content": [{"type": "text", "text": "error: %s" % exc}],
                        "isError": True}
            return {"content": [{"type": "text", "text": str(value)}]}
        return {"content": [{"type": "text", "text": "unknown tool: %s" % name}],
                "isError": True}

    def start(self):
        host = "127.0.0.1"
        httpd = HTTPServer((host, self.port), _make_handler(self.handle))
        self._httpd = httpd
        return httpd

    def serve_forever(self):
        self.start().serve_forever()

    def shutdown(self):
        if self._httpd:
            self._httpd.shutdown()


def _make_handler(handle_fn):
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                body = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                body = {}
            result = handle_fn(body)
            data = json.dumps({"jsonrpc": "2.0", "id": body.get("id"), "result": result})
            out = data.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)

        def log_message(self, *args):
            pass

    return Handler
