# MCP Experiment

This repository contains a minimal example of a Model Context Protocol (MCP) server implemented with **FastMCP**. The server exposes a single tool named `favorite_number` which always returns the string `"Lauren's favorite number is 13"`.

## Getting Started

Follow these steps to install dependencies and run the server:

1. **Install dependencies** (requires [Poetry](https://python-poetry.org/)):
   ```bash
   poetry install
   ```
2. **Start the server**:
   ```bash
   poetry run python mcp_experiment/server.py
   ```
   The server will start an SSE endpoint at [http://127.0.0.1:8000/jsonrpc](http://127.0.0.1:8000/jsonrpc).

## API Endpoint

All MCP/JSON-RPC requests are handled via a single endpoint:

- `POST /jsonrpc` – All Model Context Protocol (MCP) traffic, including tool execution, goes through this endpoint (JSON‑RPC over SSE).

## Tool Documentation

- **favorite_number**: Returns the string `"Lauren's favorite number is 13"`. Takes no parameters.
