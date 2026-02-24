# MoneyChoice MCP Server

The MoneyChoice MCP Server delivers institutional-grade economic forecasts powered by a proprietary quantum-inspired analytical framework.

## Features

- **Quantum-Driven Framework**: Evaluates multi-state market probabilities.
- **Institutional Coverage**: Inflation, Labor, Monetary Policy, GDP, FX, Commodities, Equities, and more.
- **High Accuracy**: Documented 80%+ historical accuracy since 2015.
- **MCP Native**: Full compatibility with the Model Context Protocol.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and add your API key:

```bash
MONEYCHOICE_API_KEY=your_api_key_here
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONEYCHOICE_API_KEY` | Your MoneyChoice API key | Required |
| `MONEYCHOICE_API_BASE` | API base URL | `https://api.moneychoice.us` |
| `MCP_HTTP_PORT` | Port to run HTTP server | Omit for stdio mode |
| `MCP_FORECAST_CACHE_TTL` | Cache TTL in seconds | `172800` (48 hours) |

## Usage

Run the server in stdio mode:

```bash
python macro_forecast_mcp.py
```

Or in HTTP mode:

```bash
export MCP_HTTP_PORT=9000
python macro_forecast_mcp.py
```

## License

Institutional use only. See [MoneyChoice.us](https://moneychoice.us/) for details.
