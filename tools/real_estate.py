"""
MCP tool: forecast_real_estate
Covers home prices, housing supply, permits, and mortgage rates.
"""

from __future__ import annotations

import json
from typing import Literal

import httpx

from core.server import mcp
from core.config import DEFAULT_API_KEY, Timeframe
from core.cache import _get_forecast_cached
from core.formatters import _forecast_annotations, _format_forecast_result

RealEstateIndicator = Literal[
    "case_shiller_index",
    "monthly_supply_of_houses_in_usa",
    "new_privately_owned_housing_units_authorized_in_permit",
    "30_year_fixed_mortgage",
]


@mcp.tool(name="forecast_real_estate", annotations=_forecast_annotations("Real Estate Forecast"))
async def get_macroeconomic_forecast_for_real_estate(
    indicator: RealEstateIndicator,
    timeframe: Timeframe = "monthly",
    api_key: str = DEFAULT_API_KEY,
) -> str:
    """Get macroeconomic forecast for real estate indicators.

    Returns forecast data for home prices, supply, permits, and mortgage rates.
    Use for housing and real estate outlooks.
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
