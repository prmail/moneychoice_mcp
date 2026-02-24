"""
MCP tool: forecast_commodities
Covers crude oil, natural gas, aluminium prices, and commodity volatility.
"""

from __future__ import annotations

import json
from typing import Literal

import httpx

from core.server import mcp
from core.config import DEFAULT_API_KEY, Timeframe
from core.cache import _get_forecast_cached
from core.formatters import _forecast_annotations, _format_forecast_result

CommodityIndicator = Literal[
    "crude_oil_brent_europe",
    "crude_oil_west_texas_wti",
    "henry_hub_natural_gas_spot_price",
    "ppi_aluminium_prices",
    "volatility_oil",
    "volatlity_gold",
]


@mcp.tool(name="forecast_commodities", annotations=_forecast_annotations("Commodity Forecast"))
async def get_macroeconomic_forecast_for_commodities(
    indicator: CommodityIndicator,
    timeframe: Timeframe = "monthly",
    api_key: str = DEFAULT_API_KEY,
) -> str:
    """Get macroeconomic forecast for commodity indicators.

    Returns forecast data for crude oil, natural gas, aluminium, and
    related commodity volatility. Use for commodity price and volatility outlooks.
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
