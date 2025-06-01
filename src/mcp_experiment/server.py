import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, StreamingResponse
from pydantic import BaseModel
from typing import Any, Optional
import json

app = FastAPI(title="Favorite Number MCP Server")

# NOTE: This implementation is for a single client/dev environment only.
# Global event queue for sending JSON-RPC responses to the SSE client.
event_queue: asyncio.Queue = asyncio.Queue()

class JSONRPCRequest(BaseModel):
    jsonrpc: str
    method: str
    params: Optional[Any] = None
    id: Optional[Any] = None

def make_jsonrpc_response(result: Any, id: Any):
    return {
        "jsonrpc": "2.0",
        "result": result,
        "id": id
    }

def make_jsonrpc_error(code: int, message: str, id: Any = None):
    return {
        "jsonrpc": "2.0",
        "error": {
            "code": code,
            "message": message
        },
        "id": id
    }

tools = [
    {
        "name": "favorite_number",
        "description": "Return Lauren's favorite number",
        "input_schema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
]

@app.get("/")
def root():
    return PlainTextResponse("MCP server is running.")

@app.post("/jsonrpc")
async def jsonrpc(request: Request):
    try:
        req_json = await request.json()
    except Exception:
        # Parse error
        response = make_jsonrpc_error(-32700, "Parse error", None)
        await event_queue.put(response)
        return PlainTextResponse("", status_code=202)

    # Support for batch requests is not implemented
    if isinstance(req_json, list):
        response = make_jsonrpc_error(-32600, "Batch requests not supported", None)
        await event_queue.put(response)
        return PlainTextResponse("", status_code=202)

    try:
        rpc_req = JSONRPCRequest(**req_json)
    except Exception:
        response = make_jsonrpc_error(-32600, "Invalid Request", req_json.get("id") if isinstance(req_json, dict) else None)
        await event_queue.put(response)
        return PlainTextResponse("", status_code=202)

    if rpc_req.jsonrpc != "2.0":
        response = make_jsonrpc_error(-32600, "Invalid Request: jsonrpc must be '2.0'", rpc_req.id)
        await event_queue.put(response)
        return PlainTextResponse("", status_code=202)

    method = rpc_req.method
    params = rpc_req.params
    id = rpc_req.id

    # Handle methods
    if method == "initialize":
        result = {
            "name": "FavoriteNumberServer",
            "mcp_version": "0.1",
            "capabilities": {
                "tools": True
            }
        }
        response = make_jsonrpc_response(result, id)
        await event_queue.put(response)
        return PlainTextResponse("", status_code=202)

    elif method == "tools/list":
        response = make_jsonrpc_response(tools, id)
        await event_queue.put(response)
        return PlainTextResponse("", status_code=202)

    elif method == "tools/call":
        if not isinstance(params, dict):
            response = make_jsonrpc_error(-32602, "Invalid params", id)
            await event_queue.put(response)
            return PlainTextResponse("", status_code=202)
        tool_name = params.get("tool")
        tool_args = params.get("args", {})

        if tool_name != "favorite_number":
            response = make_jsonrpc_error(-32601, "Method not found: unknown tool", id)
            await event_queue.put(response)
            return PlainTextResponse("", status_code=202)

        # favorite_number tool ignores args
        result = "Lauren's favorite number is 13"
        response = make_jsonrpc_response(result, id)
        await event_queue.put(response)
        return PlainTextResponse("", status_code=202)

    else:
        response = make_jsonrpc_error(-32601, "Method not found", id)
        await event_queue.put(response)
        return PlainTextResponse("", status_code=202)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# SSE endpoint for /jsonrpc
@app.get("/jsonrpc")
async def jsonrpc_sse():
    async def event_stream():
        # Send an initial comment to flush SSE headers so the client
        # immediately considers the stream established. Chainlit will
        # then POST the `initialize` request without hanging.
        yield ": init\n\n"
        while True:
            event = await event_queue.get()
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
