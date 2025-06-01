# MCP Experiment

This repository contains a minimal example of a Model Context Protocol (MCP) server implemented with FastAPI. The server exposes a single tool named `favorite_number` which always returns the string `"Lauren's favorite number is 13"`.

## Getting Started

Follow these steps to install dependencies and run the server:

1. **Install dependencies** (requires [Poetry](https://python-poetry.org/)):
   ```bash
   poetry install
   ```
2. **Start the server**:
   ```bash
   poetry run uvicorn mcp_experiment.server:app --reload
   ```
   The server will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoint

All MCP/JSON-RPC requests are handled via a single endpoint:

- `POST /jsonrpc` – All Model Context Protocol (MCP) traffic, including tool execution, goes through this endpoint.

### Example request

To execute the `favorite_number` tool, send a JSON-RPC request:

```bash
curl -X POST http://127.0.0.1:8000/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "favorite_number", "params": {}, "id": 1}'
```

Response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "Lauren's favorite number is 13"
}
```

## Tool Documentation

- **favorite_number**: Returns the string `"Lauren's favorite number is 13"`. Takes no parameters.
