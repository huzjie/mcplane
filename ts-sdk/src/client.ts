import { JsonRpcRequest, JsonRpcResponse, MCP_PROTOCOL_VERSION } from "./types";

export interface ClientOptions {
  token?: string;
  timeoutMs?: number;
  fetchImpl?: typeof fetch;
}

export class McplaneClient {
  private baseUrl: string;
  private token?: string;
  private timeoutMs: number;
  private fetchImpl: typeof fetch;

  constructor(baseUrl: string, options: ClientOptions = {}) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.token = options.token;
    this.timeoutMs = options.timeoutMs ?? 60_000;
    this.fetchImpl = options.fetchImpl ?? fetch;
  }

  private async request(
    serverName: string,
    method: string,
    params: Record<string, unknown>,
  ): Promise<JsonRpcResponse> {
    const payload: JsonRpcRequest = { jsonrpc: "2.0", id: 1, method, params };
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      Accept: "application/json",
      "Mcp-Method": method,
      "Mcp-Name": serverName,
      "Mcp-Protocol-Version": MCP_PROTOCOL_VERSION,
    };
    if (this.token) headers["Authorization"] = `Bearer ${this.token}`;

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);
    try {
      const resp = await this.fetchImpl(`${this.baseUrl}/mcp`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
      return (await resp.json()) as JsonRpcResponse;
    } finally {
      clearTimeout(timer);
    }
  }

  async listTools(serverName: string): Promise<JsonRpcResponse> {
    return this.request(serverName, "tools/list", {});
  }

  async callTool(
    serverName: string,
    tool: string,
    args: Record<string, unknown>,
  ): Promise<JsonRpcResponse> {
    return this.request(serverName, "tools/call", { name: tool, arguments: args });
  }

  async listPrompts(serverName: string): Promise<JsonRpcResponse> {
    return this.request(serverName, "prompts/list", {});
  }

  async listResources(serverName: string): Promise<JsonRpcResponse> {
    return this.request(serverName, "resources/list", {});
  }

  async ping(serverName: string): Promise<JsonRpcResponse> {
    return this.request(serverName, "ping", {});
  }
}
