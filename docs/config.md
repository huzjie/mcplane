# 配置

mcplane 使用 JSON 配置 + `MCPLANE_*` 环境变量覆盖（双下划线表示嵌套层级）。

```json
{
  "gateway": {"host": "0.0.0.0", "port": 8090, "upstream_timeout_s": 60},
  "registry": {"discovery_paths": ["servers.json"]},
  "auth": {"enabled": false, "mode": "ema"},
  "rate_limit": {"enabled": true, "requests_per_second": 100, "burst": 200},
  "cache": {"enabled": true, "default_ttl_ms": 60000}
}
```

环境变量示例：`MCPLANE_GATEWAY__PORT=8091` 覆盖端口。
