# 架构设计

mcplane 是一个**无状态 MCP 控制平面与网关**，面向 Model Context Protocol
2026-07-28 无状态规范。核心设计原则：**每个请求都独立可服务**，网关不在内存中
维护任何服务端会话，天然支持水平扩展与多副本负载均衡。

## 分层结构

```
客户端 (Python/TS SDK 或任意 MCP 客户端)
        │  JSON-RPC 2.0 over HTTP
        │  Mcp-Method / Mcp-Name / Mcp-Protocol-Version 头
        ▼
┌─────────────────────────────────────────┐
│  Gateway 层 (gateway/)                  │
│  · HeaderRouter 基于头路由               │
│  · StatelessProxy 无状态转发             │
│  · MultiRoundTripHandler MRTR            │
│  · LoadBalancer 负载均衡                 │
└─────────────────────────────────────────┘
        │
        ├── Policy 层 (policy/)  EMA + 限流
        ├── Auth 层 (auth/)  OIDC/JWT/APIKey
        ├── Cache 层 (cache/)  ttlMs/cacheScope
        ├── Tasks 层 (tasks/)  长任务扩展
        └── Registry 层 (registry/)  服务发现
        │
        ▼
   上游 MCP Server (任意实现)
```

## 为什么无状态

2026-07-28 规范移除了 `initialize` 握手和 `Mcp-Session-Id`，把路由与关联信息
全部上移到 HTTP 头。好处：

- 任意实例都能接任意请求，负载均衡器无需粘性会话；
- 水平扩容零状态迁移成本；
- 崩溃恢复无需重建会话；
- 网关、限流器、WAF 可以直接按 `Mcp-Method`/`Mcp-Name` 头路由与计费。
