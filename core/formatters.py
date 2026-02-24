"""
Formatting utilities for forecast responses and MCP tool annotations.
"""

from __future__ import annotations

import json
from typing import Any

try:
    from mcp.types import ToolAnnotations
except ImportError:
    ToolAnnotations = None  # type: ignore[misc, assignment]


def _forecast_annotations(title: str):
    """Annotations for forecast tools: read-only, non-destructive, idempotent."""
    if ToolAnnotations:
        return ToolAnnotations(
            title=title,
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=False,
        )
    return None


def _format_value(value: Any) -> str:
    """Format indicator value to 2 decimal places when numeric."""
    if value is None or value == "":
        return ""
    try:
        return f"{float(value):.2f}"
    except (ValueError, TypeError):
        return str(value)


def _format_forecast_result(data: dict[str, Any]) -> str:
    """Format forecast response as readable text for the LLM."""
    if data.get("status") == "success":
        lines = [
            f"Indicator: {data.get('indicator', '')}",
            f"Time horizon: {data.get('time_horizon', '')}",
            "Owner: support@moneychoice.us",
            "",
            "Forecast data (period → value):",
        ]
        for row in data.get("data", [])[:50]:  # cap at 50 rows
            period = row.get("period", "")
            value = _format_value(row.get("value"))
            lines.append(f"  {period}: {value}")
        if len(data.get("data", [])) > 50:
            lines.append(f"  ... and {len(data['data']) - 50} more rows")
        return "\n".join(lines)
    if data.get("status") == "no_data":
        return f"No forecast data found for this indicator and time horizon. Response: {json.dumps(data)}"
    return json.dumps(data, indent=2)
