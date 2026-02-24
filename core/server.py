"""
Shared FastMCP server instance.
Import `mcp` from here in all tools and resources.
"""

from __future__ import annotations

try:
    from fastmcp import FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

mcp = FastMCP("macro-economic-forecast")
