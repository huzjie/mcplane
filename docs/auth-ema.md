# 企业级统一授权（EMA）

EMA（Enterprise-Managed Authorization）让组织集中管理授权，终端用户通过单点
登录即可访问所有已连接的 MCP 服务器。

## 组件

- `auth/oidc.py` — OIDC 验证，含 RFC 9207 发行者校验（防授权服务器混淆）；
- `auth/jwt.py` — HS256 JWT 编解码（纯标准库）；
- `auth/apikey.py` — API Key 生成与校验；
- `auth/ema.py` — EMA 规则评估（principal × server × method × scopes）。

## 规则示例

```json
{"name": "allow-read", "principal": "alice", "server": "*",
 "method": "tools/list", "effect": "allow"}
```
