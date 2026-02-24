"""
MCP tool: forecast_labor
Covers unemployment, labor force participation, and employment by sector.
"""

from __future__ import annotations

import json
from typing import Literal

import httpx

from core.server import mcp
from core.config import DEFAULT_API_KEY, Timeframe
from core.cache import _get_forecast_cached
from core.formatters import _forecast_annotations, _format_forecast_result

LaborIndicator = Literal[
    "unemployment",
    "employment_population_ratio",
    "labor_force_participation_rate",
    "employees_in_manufacturing",
    "employees_in_financial_activities",
]


@mcp.tool(name="forecast_labor", annotations=_forecast_annotations("Labor Forecast"))
async def get_macroeconomic_forecast_for_labor(
    indicator: LaborIndicator,
    timeframe: Timeframe = "monthly",
    api_key: str = DEFAULT_API_KEY,
) -> str:
    """Get macroeconomic forecast for labor indicators.

    Returns forecast data for unemployment, participation, and employment.
    Use for labor market outlooks.
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
