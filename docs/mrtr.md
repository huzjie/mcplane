# 多往返请求（MRTR）

无状态规范用 MRTR 取代了需要长连接的双向流。当工具执行到一半需要用户输入时，
服务器返回 `resultType: "input_required"` 并附带问题；客户端回答后带
`inputResponses` 重新发起调用即可。

## 流程

```
client → server: tools/call (name, arguments)
server → client: { resultType: "input_required", question: "确认删除?" }
client → server: tools/call (name, arguments, inputResponses: ["yes"])
server → client: { content: [...] }
```

网关侧 `MultiRoundTripHandler` 限制最大往返次数（默认 8），防止死循环。
