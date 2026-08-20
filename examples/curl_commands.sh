#!/usr/bin/env bash
# Example curl calls against a running mcplane gateway.

GW=${GW:-http://127.0.0.1:8090}

echo "== list tools =="
curl -s -X POST "$GW/mcp" \
  -H "Content-Type: application/json" \
  -H "Mcp-Method: tools/list" \
  -H "Mcp-Name: echo" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

echo
echo "== call echo =="
curl -s -X POST "$GW/mcp" \
  -H "Content-Type: application/json" \
  -H "Mcp-Method: tools/call" \
  -H "Mcp-Name: echo" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"echo","arguments":{"text":"hi"}}}'

echo
echo "== healthz =="
curl -s "$GW/healthz"
echo
