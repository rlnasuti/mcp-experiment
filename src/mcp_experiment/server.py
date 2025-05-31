from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Any, Optional
import json

app = FastAPI(title="Favorite Number MCP Server")

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
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
]

@app.post("/jsonrpc")
async def jsonrpc(request: Request):
    try:
        req_json = await request.json()
    except Exception:
        # Parse error
        return make_jsonrpc_error(-32700, "Parse error", None)

    # Support for batch requests is not implemented
    if isinstance(req_json, list):
        return make_jsonrpc_error(-32600, "Batch requests not supported", None)

    try:
        rpc_req = JSONRPCRequest(**req_json)
    except Exception:
        return make_jsonrpc_error(-32600, "Invalid Request", req_json.get("id") if isinstance(req_json, dict) else None)

    if rpc_req.jsonrpc != "2.0":
        return make_jsonrpc_error(-32600, "Invalid Request: jsonrpc must be '2.0'", rpc_req.id)

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
        return make_jsonrpc_response(result, id)

    elif method == "tools/list":
        return make_jsonrpc_response(tools, id)

    elif method == "tools/call":
        if not isinstance(params, dict):
            return make_jsonrpc_error(-32602, "Invalid params", id)
        tool_name = params.get("tool")
        tool_args = params.get("args", {})

        if tool_name != "favorite_number":
            return make_jsonrpc_error(-32601, "Method not found: unknown tool", id)

        # favorite_number tool ignores args
        result = "Lauren's favorite number is 13"
        return make_jsonrpc_response(result, id)

    else:
        return make_jsonrpc_error(-32601, "Method not found", id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
