"""Typed MCP message payloads (dataclasses).

These map directly onto the JSON-RPC ``params``/``result`` bodies exchanged by
the stateless gateway. All models are plain dataclasses with ``to_dict`` so the
core package remains dependency-free.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class Method:
    """MCP method names used across the gateway and SDKs."""

    INITIALIZE = "initialize"
    PING = "ping"
    LIST_TOOLS = "tools/list"
    CALL_TOOL = "tools/call"
    LIST_PROMPTS = "prompts/list"
    GET_PROMPT = "prompts/get"
    LIST_RESOURCES = "resources/list"
    READ_RESOURCE = "resources/read"
    LIST_RESOURCE_TEMPLATES = "resources/templates/list"
    COMPLETE = "completion/complete"
    TASK_STATUS = "tasks/status"
    TASK_CANCEL = "tasks/cancel"


@dataclass
class Tool:
    name: str
    description: str = ""
    input_schema: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        out = {"name": self.name}
        if self.description:
            out["description"] = self.description
        if self.input_schema:
            out["inputSchema"] = self.input_schema
        return out


@dataclass
class ListToolsRequest:
    cursor: Optional[str] = None


@dataclass
class ListToolsResult:
    tools: List[Tool] = field(default_factory=list)
    next_cursor: Optional[str] = None

    def to_dict(self):
        out = {"tools": [t.to_dict() for t in self.tools]}
        if self.next_cursor:
            out["nextCursor"] = self.next_cursor
        return out


@dataclass
class ContentBlock:
    type: str = "text"
    text: str = ""
    data: Optional[str] = None
    mime_type: Optional[str] = None

    def to_dict(self):
        out = {"type": self.type}
        if self.type == "text":
            out["text"] = self.text
        if self.data is not None:
            out["data"] = self.data
        if self.mime_type:
            out["mimeType"] = self.mime_type
        return out


@dataclass
class CallToolRequest:
    name: str
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CallToolResult:
    content: List[ContentBlock] = field(default_factory=list)
    is_error: bool = False

    def to_dict(self):
        out = {"content": [c.to_dict() for c in self.content]}
        if self.is_error:
            out["isError"] = True
        return out


@dataclass
class ListPromptsResult:
    prompts: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self):
        return {"prompts": self.prompts}


@dataclass
class ListResourcesResult:
    resources: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self):
        return {"resources": self.resources}


@dataclass
class InputRequiredResult:
    """MRTR: server asks the client for additional input mid-request."""

    question: str = ""
    options: List[str] = field(default_factory=list)

    def to_dict(self):
        out = {"resultType": "input_required", "question": self.question}
        if self.options:
            out["options"] = self.options
        return out


@dataclass
class InputResponses:
    responses: List[str] = field(default_factory=list)

    def to_dict(self):
        return {"inputResponses": self.responses}


@dataclass
class TaskStatusResult:
    task_id: str = ""
    status: str = "running"
    result: Optional[Any] = None
    error: Optional[str] = None

    def to_dict(self):
        out = {"taskId": self.task_id, "status": self.status}
        if self.result is not None:
            out["result"] = self.result
        if self.error:
            out["error"] = self.error
        return out


@dataclass
class CancellationResult:
    cancelled: bool = True

    def to_dict(self):
        return {"cancelled": self.cancelled}
