<div align="center">

# mcplane

**无状态 MCP 控制平面与网关** · Stateless MCP Control Plane & Gateway

面向 Model Context Protocol **2026-07-28 无状态规范**的生产级控制平面

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![CI](https://github.com/huzjie/mcplane/actions/workflows/ci.yml/badge.svg)](https://github.com/huzjie/mcplane/actions)
[![Spec](https://img.shields.io/badge/MCP%20Spec-2026--07--28-red.svg)](#)

</div>

## 这是什么？

2026 年 7 月 28 日，MCP 迎来史上最大规模的「史诗级更新」——协议层彻底**无状态化**：
`initialize` 握手被移除、`Mcp-Session-Id` 被移除，路由与关联信息全部上移到 HTTP 头
（`Mcp-Method` / `Mcp-Name`），并引入 **MRTR 多往返请求**、**列表结果缓存**
（`ttlMs` + `cacheScope`）、**OAuth 2.0/OIDC 加固**（RFC 9207）以及正式扩展框架
（MCP Apps、Tasks 长任务）。企业侧呼声最高的 **EMA（企业级统一授权）** 同期转正。

**mcplane** 就是为这个无状态时代打造的**控制平面与网关**：它帮你把任意数量的 MCP
服务器统一接入、按头路由、集中鉴权授权、限流、缓存与观测——每一个请求都独立可
服务，天然支持多副本水平扩展。

> 项目约 **170 个文件**，核心包 `mcplane/` **零第三方运行时依赖**（纯 Python 标准
> 库），开箱即用；FastAPI 控制面、React 控制台、Python/TS 双 SDK、Docker/K8s/Helm
> 全部就绪。

## 核心能力

| 模块 | 说明 |
|------|------|
| **无状态网关** | 基于 `Mcp-Method`/`Mcp-Name` 头的路由，无服务端会话 |
| **MRTR** | 多往返请求，`input_required` / `inputResponses` 交互闭环 |
| **EMA 统一授权** | principal × server × method × scopes 规则，零信任默认拒绝 |
| **OIDC/JWT** | HS256 JWT + RFC 9207 发行者校验 + API Key |
| **限流** | 线程安全令牌桶，支持突发（burst） |
| **列表缓存** | `ttlMs` + `cacheScope` 语义，确定性排序 |
| **长任务** | MCP Tasks 扩展，任务生命周期管理 |
| **可观测** | Prometheus 指标 + W3C traceparent 追踪 |
| **注册中心** | `servers.json` 发现 + SQLite 持久化 |
| **多语言 SDK** | Python（同步/异步）+ TypeScript |
| **Web 控制台** | React 深色主题，可视化工具发现与调用 |

## 架构

```
客户端 (Python/TS SDK / 任意 MCP 客户端)
   │  JSON-RPC 2.0 over HTTP + Mcp-* 头
   ▼
┌──────────────────────────────────────────┐
│  Gateway  gateway/                       │
│   HeaderRouter · StatelessProxy          │
│   MultiRoundTripHandler · LoadBalancer   │
└──────────────────────────────────────────┘
   │        │         │         │
   ▼        ▼         ▼         ▼
 policy/   auth/     cache/    tasks/
 限流      EMA/OIDC   ttlMs   长任务
   │
   ▼
 registry/ (servers.json + SQLite)
   │
   ▼
 上游 MCP Server (echo / calculator / ...)
```

## 快速开始

```bash
# 1. 安装（核心零依赖）
pip install -e .

# 2. 校验环境
mcplane doctor

# 3. 启动一个 mock MCP 服务器（另开终端）
python -m mcplane.mock --port 8100

# 4. 启动网关
mcplane serve

# 5. 调用工具
mcplane call --server echo --tool echo --arguments '{"text":"hello stateless MCP"}'
mcplane call --server echo --tool calculator --arguments '{"expression":"1+2*3"}'
```

Python SDK：

```python
from mcplane.sdk.client import McplaneClient

client = McplaneClient("http://127.0.0.1:8090")
print(client.list_tools("echo"))
print(client.call_tool("echo", "echo", {"text": "hello"}))
```

TypeScript SDK：

```ts
import { McplaneClient } from "@mcplane/sdk";
const c = new McplaneClient("http://127.0.0.1:8090");
console.log(await c.callTool("echo", "echo", { text: "hello" }));
```

## 配置

JSON 配置 + `MCPLANE_*` 环境变量覆盖（`__` 表示层级）：

```json
{
  "gateway": {"host": "0.0.0.0", "port": 8090, "upstream_timeout_s": 60},
  "registry": {"discovery_paths": ["servers.json"]},
  "auth": {"enabled": false, "mode": "ema"},
  "rate_limit": {"enabled": true, "requests_per_second": 100, "burst": 200},
  "cache": {"enabled": true, "default_ttl_ms": 60000}
}
```

## 部署

```bash
# Docker
docker build -t mcplane . && docker run -p 8090:8090 mcplane

# Kubernetes
kubectl apply -f k8s/

# Helm
helm install mcplane ./helm/mcplane
```

## 目录结构

```
mcplane/
├── mcplane/            # Python 核心包（零依赖）
│   ├── spec/           #   MCP 协议模型 + 头定义
│   ├── gateway/        #   无状态网关（路由/代理/MRTR/负载均衡）
│   ├── registry/       #   服务注册与发现
│   ├── auth/           #   JWT/OIDC/APIKey/EMA
│   ├── policy/         #   策略引擎 + 限流
│   ├── cache/          #   TTL 缓存 + 列表缓存
│   ├── tasks/          #   长任务扩展
│   ├── observability/  #   指标 + 追踪
│   ├── storage/        #   SQLite 持久化
│   ├── cli/            #   命令行
│   ├── sdk/            #   Python 同步/异步客户端
│   └── server/         #   网关 HTTP 服务 + mock 服务器
├── ts-sdk/             # TypeScript SDK
├── console/            # React 深色控制台
├── k8s/                # Kubernetes 清单
├── helm/mcplane/       # Helm chart
├── docs/               # 20+ 篇文档
├── tests/              # pytest 测试套件
└── examples/           # 配置与 SDK 示例
```

## 文档

见 [`docs/`](docs/)：架构、无状态迁移、MRTR、EMA 授权、部署、API 参考、CLI、
配置、SDK（Python/TS）、指标、长任务、安全、测试等 20+ 篇。

## 测试

```bash
pip install -e ".[test]"
pytest
```

## License

[Apache 2.0](LICENSE)
