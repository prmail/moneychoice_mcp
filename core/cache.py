"""
In-memory caching layer for forecast API responses.
Avoids calling the API/DB unless the cache is stale.

Cache TTL and version-file invalidation are controlled via:
  - MCP_FORECAST_CACHE_TTL:      TTL in seconds (default 172800 = 48 hours). Set to 0 to disable.
  - MCP_FORECAST_VERSION_FILE:   path to a file; when its mtime changes, cache is invalidated.
                                  After updating forecast data, run: touch /path/to/this/file
"""

from __future__ import annotations

import os
import time
from typing import Any

from .config import CACHE_TTL, VERSION_FILE
from .client import _call_forecast_api

# In-memory cache: key (indicator_name, time_horizon, api_key) -> {"data": dict, "cached_at": float}
_forecast_cache: dict[tuple[str, str, str], dict[str, Any]] = {}

# Last known mtime of VERSION_FILE; when it increases we clear the cache
_version_file_mtime: float = 0.0


def _check_version_file_and_invalidate() -> None:
    """If VERSION_FILE is set and its mtime is newer than our last known, clear the cache."""
    global _version_file_mtime
    if not VERSION_FILE:
        return
    try:
        mtime = os.path.getmtime(VERSION_FILE)
        if mtime > _version_file_mtime:
            _forecast_cache.clear()
            _version_file_mtime = mtime
    except OSError:
        pass


async def _get_forecast_cached(
    api_key: str,
    indicator_name: str,
    time_horizon: str,
) -> dict[str, Any]:
    """Return forecast from cache or call API and cache the result. No API/DB call when cache is valid."""
    ind = indicator_name.strip().lower()
    th = time_horizon.strip().lower()
    key = (ind, th, api_key)

    if CACHE_TTL > 0:
        _check_version_file_and_invalidate()
        entry = _forecast_cache.get(key)
        if entry:
            if time.time() - entry["cached_at"] <= CACHE_TTL:
                return entry["data"]
            # Expired; remove and refetch below
            _forecast_cache.pop(key, None)

    data = await _call_forecast_api(api_key, indicator_name, time_horizon)
    if CACHE_TTL > 0:
        _forecast_cache[key] = {"data": data, "cached_at": time.time()}
    return data
