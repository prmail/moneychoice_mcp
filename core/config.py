"""
Configuration and environment variable loading.
All constants and type aliases used across the project live here.
"""

from __future__ import annotations

import os
from typing import Literal

# API base URL (override with MONEYCHOICE_API_BASE env var)
API_BASE = os.environ.get("MONEYCHOICE_API_BASE", "https://api.moneychoice.us")
FORECAST_URL = f"{API_BASE.rstrip('/')}/moneychoice_complete.api?x=getmacroeconomicforecast"

# Default API key for the tool (can be overridden per call)
DEFAULT_API_KEY = os.environ.get("MONEYCHOICE_API_KEY", "")

# Cache: TTL in seconds (0 = disable). Default 48 hours.
CACHE_TTL = int(os.environ.get("MCP_FORECAST_CACHE_TTL", "172800"))

# Optional: when this file's mtime changes, cache is invalidated (touch it after updating forecast data).
VERSION_FILE = os.environ.get("MCP_FORECAST_VERSION_FILE", "").strip() or None

# Type alias for timeframe
Timeframe = Literal["monthly", "quarterly", "yearly"]
