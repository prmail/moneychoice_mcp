"""
MCP tool: forecast_rates
Covers Fed funds rate, Treasury yields, SOFR, and yield spreads.
"""

from __future__ import annotations

import json
from typing import Literal

import httpx

from core.server import mcp
from core.config import DEFAULT_API_KEY, Timeframe
from core.cache import _get_forecast_cached
from core.formatters import _forecast_annotations, _format_forecast_result

InterestRateIndicator = Literal[
    "fed_funds_effective_rate",
    "10_year_yield",
    "sofr",
    "30_day_aa_financial_commercial_paper_interest_rate",
    "discount_window_primary_credit_rate",
    "bank_prime_loan_rate",
    "10_year_treasury_minus_2_year_treasury",
    "10_year_treasury_minus_federal_funds_rate",
]


@mcp.tool(name="forecast_rates", annotations=_forecast_annotations("Rates Forecast"))
async def get_macroeconomic_forecast_for_interest_rates_and_bond_yields(
    indicator: InterestRateIndicator,
    timeframe: Timeframe = "monthly",
    api_key: str = DEFAULT_API_KEY,
) -> str:
    """Get macroeconomic forecast for interest rates and bond yield indicators.

    Returns forecast data for Fed funds, Treasury yields, SOFR, and spreads.
    Use for rates outlooks.
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
