"""
HTTP client for the MoneyChoice forecast API.
Contains the raw (no cache) API call function.
"""

from __future__ import annotations

from typing import Any

import httpx

from .config import FORECAST_URL


async def _call_forecast_api(
    api_key: str,
    indicator_name: str,
    time_horizon: str,
) -> dict[str, Any]:
    """Call the forecast service (no cache)."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            FORECAST_URL,
            json={
                "api_key": api_key,
                "indicator_name": indicator_name.strip().lower(),
                "time_horizon": time_horizon.strip().lower(),
            },
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()
