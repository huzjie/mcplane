# API 参考

## HTTP 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/mcp` | 无状态 MCP JSON-RPC 入口 |
| GET | `/healthz` | 健康检查 |
| GET | `/metrics` | Prometheus 指标 |

## 请求头

| 头 | 必需 | 说明 |
|----|------|------|
| `Mcp-Method` | 是 | MCP 方法名 |
| `Mcp-Name` | 否 | 目标服务器名 |
| `Mcp-Protocol-Version` | 是 | 固定 `2026-07-28` |
| `Authorization` | 否 | `Bearer <token>` |
| `Idempotency-Key` | 否 | 幂等键 |
| `X-Trace-Id` | 否 | 追踪 ID |
