# 可观测性

`/metrics` 端点输出 Prometheus 文本格式指标：

- `mcplane_requests_total` — 请求总数
- `mcplane_errors_total` — 错误总数
- `mcplane_round_trips_total` — MRTR 往返次数
- `mcplane_cache_hits_total` / `mcplane_cache_misses_total`
- `mcplane_latency_seconds_summary` — 网关延迟
- `mcplane_upstream_latency_seconds_summary` — 上游延迟
