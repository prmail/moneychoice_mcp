"""
MCP server — entry point.

All tools and resources are defined in their own modules:
  core/       — server instance, config, HTTP client, cache, formatters
  resources/  — MoneyChoice overview resource
  tools/      — one file per forecast category (10 tools total)

Environment variables:
  MONEYCHOICE_API_BASE        Override API base URL (default: https://api.moneychoice.us)
  MONEYCHOICE_API_KEY         Your MoneyChoice API key
  MCP_FORECAST_CACHE_TTL      Cache TTL in seconds (default 172800 = 48 h). Set 0 to disable.
  MCP_FORECAST_VERSION_FILE   Path to a file; touch it to invalidate the cache.
  MCP_HTTP_PORT               Run as HTTP server on this port (omit for stdio mode).
  MCP_HTTP_HOST               HTTP bind host (default 0.0.0.0).
"""

from __future__ import annotations

import os

from core.server import mcp  # shared FastMCP instance

# Register all resources and tools by importing their modules.
# The @mcp.resource / @mcp.tool decorators execute at import time.
import resources.overview  # noqa: F401
import tools.commodities    # noqa: F401
import tools.currency       # noqa: F401
import tools.equities       # noqa: F401
import tools.gdp            # noqa: F401
import tools.inflation      # noqa: F401
import tools.rates          # noqa: F401
import tools.labor          # noqa: F401
import tools.manufacturing  # noqa: F401
import tools.real_estate    # noqa: F401
import tools.retail         # noqa: F401


def main() -> None:
    """Run the MCP server in HTTP or stdio mode."""
    http_port = os.environ.get("MCP_HTTP_PORT")
    if http_port:
        port = int(http_port)
        host = os.environ.get("MCP_HTTP_HOST", "0.0.0.0")
        # stateless_http=True: each request completes as a normal HTTP req/resp;
        # works better with HTTP/1.1 proxies and avoids Cursor's 60s timeout.
        mcp.run(transport="http", host=host, port=port, stateless_http=True)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
