# MCP Experiment

This repository contains a minimal example of a Model Context Protocol (MCP) server implemented with FastAPI. The server exposes a single tool named `favorite_number` which always returns the string `"Lauren's favorite number is 13"`.

## Running the server

Install dependencies using `poetry` and run the application with `uvicorn`:

```bash
poetry install
poetry run uvicorn mcp_experiment.server:app --reload
```

The server will start on `http://127.0.0.1:8000`.

## Endpoints

- `GET /handshake` – returns MCP handshake information including available tools.
- `POST /execute` – execute a tool by name.

Example request to execute the tool:

```bash
curl -X POST http://127.0.0.1:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"tool": "favorite_number"}'
```

Response:

```json
{"result": "Lauren's favorite number is 13"}
```
