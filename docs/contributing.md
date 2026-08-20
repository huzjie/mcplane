# 贡献指南

1. Fork 本仓库；
2. 创建特性分支；
3. 编写代码与测试（`pytest` 全绿）；
4. 提交 PR。

核心包 `mcplane/` 保持零第三方运行时依赖（stdlib only）；服务端可选依赖
（FastAPI）放在 `server` extra 中。
