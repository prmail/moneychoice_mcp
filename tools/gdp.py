"""
MCP tool: forecast_gdp
Covers GDP nowcasts from Atlanta Fed and St. Louis Fed.
"""

from __future__ import annotations

import json
from typing import Literal

import httpx

from core.server import mcp
from core.config import DEFAULT_API_KEY, Timeframe
from core.cache import _get_forecast_cached
from core.formatters import _forecast_annotations, _format_forecast_result

GDPIndicator = Literal[
    "gdp_nowcast_from_atlanta_fed",
    "real_gdp_nowcast_from_st_louis_fed",
]


@mcp.tool(name="forecast_gdp", annotations=_forecast_annotations("GDP Forecast"))
async def get_macroeconomic_forecast_for_gdp(
    indicator: GDPIndicator,
    timeframe: Timeframe = "monthly",
    api_key: str = DEFAULT_API_KEY,
) -> str:
    """Get macroeconomic forecast for GDP indicators.

    Returns forecast data for GDP nowcasts. Use for growth outlooks.
    """
    try:
        data = await _get_forecast_cached(api_key, indicator, timeframe)
        return _format_forecast_result(data)
    except httpx.HTTPStatusError as e:
        try:
            err_body = e.response.json()
            return json.dumps(err_body, indent=2)
        except Exception:
            return f"Service error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"Error fetching forecast: {e!s}"
