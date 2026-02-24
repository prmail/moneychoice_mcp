"""
MCP tool: forecast_inflation
Covers CPI, PPI, inflation expectations, and breakeven rates.
"""

from __future__ import annotations

import json
from typing import Literal

import httpx

from core.server import mcp
from core.config import DEFAULT_API_KEY, Timeframe
from core.cache import _get_forecast_cached
from core.formatters import _forecast_annotations, _format_forecast_result

InflationIndicator = Literal[
    "inflation_cpi",
    "inflation_ppi",
    "inflation_expectation_univ_of_mich",
    "cpi_urban_consumers_for_computers_and_smart_home",
    "treasury_long_term_average_inflation_indexed",
    "5_year_breakeven_inflation_rate",
    "5_year_forward_inflation_expectation_rate",
]


@mcp.tool(name="forecast_inflation", annotations=_forecast_annotations("Inflation Forecast"))
async def get_macroeconomic_forecast_for_inflation(
    indicator: InflationIndicator,
    timeframe: Timeframe = "monthly",
    api_key: str = DEFAULT_API_KEY,
) -> str:
    """Get macroeconomic forecast for inflation indicators.

    Returns forecast data for CPI, PPI, inflation expectations, and breakevens.
    Use for inflation outlooks.
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
