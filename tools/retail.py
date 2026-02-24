"""
MCP tool: forecast_retail
Covers retail sales and University of Michigan consumer sentiment.
"""

from __future__ import annotations

import json
from typing import Literal

import httpx

from core.server import mcp
from core.config import DEFAULT_API_KEY, Timeframe
from core.cache import _get_forecast_cached
from core.formatters import _forecast_annotations, _format_forecast_result

RetailIndicator = Literal[
    "advance_retail_and_food_services_sales",
    "consumer_sentiment_univ_of_michigan",
]


@mcp.tool(name="forecast_retail", annotations=_forecast_annotations("Retail Forecast"))
async def get_macroeconomic_forecast_for_retail(
    indicator: RetailIndicator,
    timeframe: Timeframe = "monthly",
    api_key: str = DEFAULT_API_KEY,
) -> str:
    """Get macroeconomic forecast for retail and consumer indicators.

    Returns forecast data for retail sales and consumer sentiment.
    Use for consumer spending outlooks.
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
