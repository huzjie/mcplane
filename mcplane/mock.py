"""Run the built-in mock MCP server: ``python -m mcplane.mock``."""

import argparse

from .server.mock_server import MockMcpServer


def main():
    parser = argparse.ArgumentParser(description="mcplane mock MCP server")
    parser.add_argument("--port", type=int, default=8100)
    args = parser.parse_args()
    print("mock MCP server listening on http://127.0.0.1:%d/mcp" % args.port)
    MockMcpServer(port=args.port).serve_forever()


if __name__ == "__main__":
    main()
