/** JSON-RPC 2.0 + MCP stateless message types. */

export interface JsonRpcRequest {
  jsonrpc: "2.0";
  id: number | string | null;
  method: string;
  params?: Record<string, unknown>;
}

export interface ContentBlock {
  type: string;
  text?: string;
  data?: string;
  mimeType?: string;
}

export interface Tool {
  name: string;
  description?: string;
  inputSchema?: Record<string, unknown>;
}

export interface ListToolsResult {
  tools: Tool[];
  nextCursor?: string;
}

export interface CallToolResult {
  content: ContentBlock[];
  isError?: boolean;
}

export interface JsonRpcResponse {
  jsonrpc: "2.0";
  id: number | string | null;
  result?: unknown;
  error?: { code: number; message: string; data?: unknown };
}

export const MCP_PROTOCOL_VERSION = "2026-07-28";
