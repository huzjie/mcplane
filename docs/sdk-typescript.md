# TypeScript SDK

```ts
import { McplaneClient } from "@mcplane/sdk";

const client = new McplaneClient("http://127.0.0.1:8090");
const tools = await client.listTools("echo");
const result = await client.callTool("echo", "echo", { text: "hello" });
```
