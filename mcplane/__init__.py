"""
mcplane - Stateless MCP Control Plane & Gateway.

A production-grade control plane for the Model Context Protocol (MCP)
2026-07-28 stateless specification: no server-side sessions, header-based
routing, multi round-trip requests (MRTR), cacheable list results, and
Enterprise-Managed Authorization (EMA).
"""

from ._version import __version__

__all__ = ["__version__"]
