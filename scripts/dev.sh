#!/usr/bin/env bash
set -euo pipefail

echo "==> Starting mock MCP server on :8100 (background)"
python -m mcplane.mock --port 8100 &
MOCK_PID=$!
trap 'kill $MOCK_PID 2>/dev/null || true' EXIT

sleep 1
echo "==> Starting gateway on :8090"
mcplane serve
