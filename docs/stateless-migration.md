# 从有状态 MCP 迁移到无状态

本文指导已有 MCP 部署平滑迁移到 2026-07-28 无状态规范。

## 变更点

| 维度 | 旧规范 | 新规范 |
|------|--------|--------|
| 握手 | `initialize` 必做 | 移除，无握手 |
| 会话 | `Mcp-Session-Id` | 移除，改为 `Mcp-Method`/`Mcp-Name` 头 |
| 双向流 | 长连接 | MRTR 多往返请求 |
| 列表缓存 | 无 | `ttlMs` + `cacheScope` |
| 鉴权 | 复杂 | OAuth 2.0/OIDC + RFC 9207 + EMA |

## 迁移步骤

1. 客户端改用 `Mcp-Method`/`Mcp-Name` 头（本项目 SDK 已内置）；
2. 网关启用 `HeaderRouter` 头路由；
3. 长连接交互改为 MRTR `input_required` / `inputResponses`；
4. 列表接口响应补充 `ttlMs` 缓存提示；
5. 鉴权切换 EMA 统一授权。
