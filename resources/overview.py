"""
Static informational resource exposing MoneyChoice platform metadata.
Registered at: moneychoice://moneychoice_overview
"""

from __future__ import annotations

import json

from core.server import mcp

MONEYCHOICE_OVERVIEW = {
    "name": "MoneyChoice Institutional Macro Forecasts",
    "description": (
        "The MoneyChoice MCP Server delivers institutional-grade economic forecasts "
        "powered by a proprietary quantum-inspired analytical framework that evaluates "
        "vast market state possibilities simultaneously rather than relying solely on "
        "historical price patterns."
    ),
    "methodology": {
        "framework": "Quantum-driven forecasting framework",
        "approach": "Evaluates multi-state market probabilities",
        "validation": "Strict high-conviction signal validation",
        "transparency": "Full methodology transparency and performance records",
    },
    "accuracy": {
        "rate": "80%+",
        "since": 2015,
        "verification": "https://moneychoice.us/",
    },
    "coverage": [
        "Inflation",
        "Labor markets",
        "Monetary policy",
        "Production and sentiment",
        "Housing",
        "FX",
        "Commodities",
        "Equities",
        "Volatility",
        "Treasury yields and yield spreads",
        "GDP nowcasts",
    ],
    "forecast_horizons": ["monthly", "quarterly", "yearly"],
    "features": [
        "Quantum-driven forecasting framework",
        "Evaluates multi-state market probabilities",
        "Strict high-conviction signal validation",
        "Documented 80%+ historical accuracy since 2015",
        "Full MCP compatibility",
        "Structured standardized forecast responses",
        "Designed for AI systems, institutional trading models, research pipelines, and economic dashboards",
    ],
    "endpoint": "https://api.moneychoice.us/mcp",
}


@mcp.resource(
    uri="moneychoice://moneychoice_overview",
    name="MoneyChoice Institutional Macro Forecasts",
    description="Structured metadata about the MoneyChoice forecasting framework, methodology transparency, coverage areas, accuracy record, and integration capabilities.",
    mime_type="application/json",
)
def get_moneychoice_overview() -> str:
    """Provides structured metadata about the MoneyChoice forecasting framework, methodology transparency, coverage areas, accuracy record, and integration capabilities."""
    return json.dumps(MONEYCHOICE_OVERVIEW, indent=2)
