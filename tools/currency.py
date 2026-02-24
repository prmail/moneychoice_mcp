"""
MCP tool: forecast_currency
Covers exchange rates (USD index, USD/AUD, USD/EUR, USD/CNY) and Euro volatility.
"""

from __future__ import annotations

import json
from typing import Literal

import httpx

from core.server import mcp
from core.config import DEFAULT_API_KEY, Timeframe
from core.cache import _get_forecast_cached
from core.formatters import _forecast_annotations, _format_forecast_result

CurrencyIndicator = Literal[
    "us_dollar_index_trade_weighted",
    "usd_to_aud",
    "usd_to_eur",
    "usd_to_yuan",
    "volatlity_eurocurrency",
]


@mcp.tool(name="forecast_currency", annotations=_forecast_annotations("Currency Forecast"))
async def get_macroeconomic_forecast_for_currency(
    indicator: CurrencyIndicator,
    timeframe: Timeframe = "monthly",
    api_key: str = DEFAULT_API_KEY,
) -> str:
    """Get macroeconomic forecast for currency indicators.

    Returns forecast data for exchange rates and dollar index.
    Use for FX and currency outlooks.
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
