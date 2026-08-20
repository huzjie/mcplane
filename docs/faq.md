# FAQ

**Q: 需要安装依赖吗？**
核心包零依赖，开箱即用。FastAPI 控制面可选。

**Q: 如何接入自己的 MCP 服务器？**
在 `servers.json` 注册 `name` 与 `url`，然后经 `/mcp` 用 `Mcp-Name` 头路由。

**Q: 支持有状态的旧服务器吗？**
网关会忽略 `Mcp-Session-Id` 并告警，仍可转发，但不保证旧会话语义。
