# 快速开始

```bash
# 1. 安装
pip install -e .

# 2. 校验
mcplane doctor

# 3. 启动 mock 服务器（另开终端）
python -m mcplane.server.mock_server

# 4. 启动网关
mcplane serve

# 5. 调用
mcplane call --server echo --tool echo --arguments '{"text":"hello"}'
```
