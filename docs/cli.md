# CLI 参考

```bash
mcplane version    # 打印版本
mcplane doctor     # 校验配置
mcplane serve      # 启动网关
mcplane register --name echo --url http://127.0.0.1:8100/mcp
mcplane list       # 列出已注册服务器
mcplane call --server echo --tool echo --arguments '{"text":"hi"}'
mcplane token --subject admin --scopes "mcp:read"
mcplane cache      # 查看缓存
```
