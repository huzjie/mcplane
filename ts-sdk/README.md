# @mcplane/sdk

TypeScript SDK for the mcplane stateless MCP control plane.

```ts
import { McplaneClient } from "@mcplane/sdk";

const client = new McplaneClient("http://127.0.0.1:8090");
const tools = await client.listTools("echo");
console.log(tools);
```
