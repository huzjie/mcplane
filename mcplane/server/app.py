"""HTTP server for the stateless gateway.

Prefers FastAPI + uvicorn when available (for a rich control plane); otherwise
falls back to a stdlib ``http.server`` implementation so the gateway runs with
zero third-party dependencies.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict

from ..config import load_config
from ..gateway.router import HeaderRouter
from ..gateway.proxy import StatelessProxy
from ..gateway.mrtr import MultiRoundTripHandler
from ..registry.server_registry import ServerRegistry
from ..registry.discovery import discover_servers
from ..spec.headers import (
    HEADER_METHOD,
    HEADER_NAME,
    HEADER_AUTHORIZATION,
    HEADER_TRACE_ID,
)
from ..spec.protocol import MCP_ERROR_CODES
from ..observability.metrics import Metrics


class Gateway:
    """Core gateway logic (transport-agnostic)."""

    def __init__(self, config: Dict):
        self.config = config
        self.registry = ServerRegistry()
        discover_servers(self.registry, config["registry"]["discovery_paths"])
        self.router = HeaderRouter(self.registry)
        self.proxy = StatelessProxy(config["gateway"]["upstream_timeout_s"])
        self.mrtr = MultiRoundTripHandler(config["gateway"]["max_round_trips"])
        self.metrics = Metrics()

    def handle(self, body: Dict, headers: Dict) -> Dict:
        method = body.get("method", "")
        self.metrics.requests_total.inc()
        server_name = headers.get(HEADER_NAME.lower()) or headers.get(HEADER_NAME)
        if not server_name:
            rec = self.router.next_by_round_robin()
        else:
            rec = self.router.resolve(server_name)
        if not rec:
            self.metrics.errors_total.inc()
            return {"error": {"code": MCP_ERROR_CODES["METHOD_NOT_FOUND"],
                              "message": "no upstream server available"}}
        result = self.proxy.forward(
            rec.url, method, body,
            headers={
                HEADER_METHOD: method,
                HEADER_NAME: rec.name,
                HEADER_AUTHORIZATION: headers.get(HEADER_AUTHORIZATION.lower()),
                HEADER_TRACE_ID: headers.get(HEADER_TRACE_ID.lower()),
            },
        )
        return result


def run_server(config: Dict, host: str = None, port: int = None):
    host = host or config["gateway"]["host"]
    port = port or config["gateway"]["port"]
    gw = Gateway(config)
    handler = _make_stdlib_handler(gw)
    httpd = HTTPServer((host, port), handler)
    print("mcplane gateway listening on http://%s:%s" % (host, port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


def _make_stdlib_handler(gateway: Gateway):
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                body = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                body = {}
            headers = {k.lower(): v for k, v in self.headers.items()}
            result = gateway.handle(body, headers)
            resp = {"jsonrpc": "2.0", "id": body.get("id")}
            if "error" in result:
                resp["error"] = result["error"]
            else:
                resp["result"] = result.get("result", result)
            out = json.dumps(resp).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)

        def do_GET(self):
            if self.path == "/healthz":
                out = b"ok"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(out)))
                self.end_headers()
                self.wfile.write(out)
            elif self.path == "/metrics":
                out = gateway.metrics.prometheus_text().encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(out)))
                self.end_headers()
                self.wfile.write(out)
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, *args):
            pass

    return Handler


def create_fastapi_app(config: Dict = None):
    """Return a FastAPI app if fastapi is installed; else raise ImportError."""
    try:
        from fastapi import FastAPI, Request
    except ImportError as exc:
        raise ImportError("fastapi is not installed; install 'mcplane[server]'") from exc
    cfg = config or load_config()
    gw = Gateway(cfg)
    app = FastAPI(title="mcplane", version="1.0.0")

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.get("/metrics")
    def metrics():
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(gw.metrics.prometheus_text())

    @app.post("/mcp")
    async def mcp(request: Request):
        body = await request.json()
        headers = {k.lower(): v for k, v in request.headers.items()}
        return gw.handle(body, headers)

    return app
