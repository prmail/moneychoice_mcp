"""
MCP tool: forecast_manufacturing
Covers durable goods, new orders, and industrial production.
"""

from __future__ import annotations

import json
from typing import Literal

import httpx

from core.server import mcp
from core.config import DEFAULT_API_KEY, Timeframe
from core.cache import _get_forecast_cached
from core.formatters import _forecast_annotations, _format_forecast_result

ManufacturingIndicator = Literal[
    "durable_goods",
    "new_orders_in_manufacturing_excluding_defence",
    "industrial_production_manufacturing_non_durable_goods",
]


@mcp.tool(name="forecast_manufacturing", annotations=_forecast_annotations("Manufacturing Forecast"))
async def get_macroeconomic_forecast_for_manufacturing(
    indicator: ManufacturingIndicator,
    timeframe: Timeframe = "monthly",
    api_key: str = DEFAULT_API_KEY,
) -> str:
    """Get macroeconomic forecast for manufacturing indicators.

    Returns forecast data for durable goods, new orders, and industrial production.
    Use for manufacturing sector outlooks.
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
