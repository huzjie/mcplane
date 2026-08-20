"""JSON-RPC 2.0 primitives and MCP protocol constants.

Reflects the MCP 2026-07-28 stateless specification: the transport layer is a
plain JSON-RPC 2.0 message envelope, with routing information carried in HTTP
headers rather than an in-band session.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

JSONRPC_VERSION = "2.0"
MCP_PROTOCOL_VERSION = "2026-07-28"

# Standard JSON-RPC 2.0 error codes (RFC 9091-ish, subset used by MCP).
MCP_ERROR_CODES = {
    "PARSE_ERROR": -32700,
    "INVALID_REQUEST": -32600,
    "METHOD_NOT_FOUND": -32601,
    "INVALID_PARAMS": -32602,
    "INTERNAL_ERROR": -32603,
}


@dataclass
class JsonRpcRequest:
    jsonrpc: str = JSONRPC_VERSION
    method: str = ""
    id: Optional[Any] = None
    params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "JsonRpcRequest":
        if obj.get("jsonrpc") != JSONRPC_VERSION:
            raise ValueError("unsupported jsonrpc version")
        if "method" not in obj:
            raise ValueError("missing method")
        return cls(
            jsonrpc=obj["jsonrpc"],
            method=obj["method"],
            id=obj.get("id"),
            params=obj.get("params") or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        out = {"jsonrpc": self.jsonrpc, "method": self.method}
        if self.id is not None:
            out["id"] = self.id
        if self.params:
            out["params"] = self.params
        return out


@dataclass
class JsonRpcErrorObject:
    code: int = -32603
    message: str = "Internal error"
    data: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        out = {"code": self.code, "message": self.message}
        if self.data is not None:
            out["data"] = self.data
        return out


@dataclass
class JsonRpcResponse:
    jsonrpc: str = JSONRPC_VERSION
    id: Optional[Any] = None
    result: Optional[Any] = None
    error: Optional[JsonRpcErrorObject] = None

    def to_dict(self) -> Dict[str, Any]:
        out = {"jsonrpc": self.jsonrpc, "id": self.id}
        if self.error is not None:
            out["error"] = self.error.to_dict()
        else:
            out["result"] = self.result
        return out


def make_response(request: JsonRpcRequest, result: Any) -> JsonRpcResponse:
    return JsonRpcResponse(id=request.id, result=result)


def make_error(request: JsonRpcRequest, code: int, message: str,
               data: Any = None) -> JsonRpcResponse:
    return JsonRpcResponse(
        id=request.id,
        error=JsonRpcErrorObject(code=code, message=message, data=data),
    )
