"""Exception hierarchy for mcplane."""


class McplaneError(Exception):
    """Base class for all mcplane errors."""

    code = "MCPLANE_ERROR"

    def __init__(self, message="", code=None):
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class ConfigError(McplaneError):
    code = "CONFIG_ERROR"


class ProtocolError(McplaneError):
    code = "PROTOCOL_ERROR"


class NotFoundError(McplaneError):
    code = "NOT_FOUND"


class AuthError(McplaneError):
    code = "AUTH_ERROR"


class ForbiddenError(McplaneError):
    code = "FORBIDDEN"


class RateLimitError(McplaneError):
    code = "RATE_LIMITED"


class UpstreamError(McplaneError):
    code = "UPSTREAM_ERROR"


class TimeoutError(McplaneError):
    code = "TIMEOUT"


class RegistryError(McplaneError):
    code = "REGISTRY_ERROR"


class TaskError(McplaneError):
    code = "TASK_ERROR"


class JsonRpcError(McplaneError):
    """JSON-RPC 2.0 error with a numeric code."""

    def __init__(self, rpc_code=-32603, message="Internal error", data=None):
        super().__init__(message)
        self.rpc_code = rpc_code
        self.data = data
