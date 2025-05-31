from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Favorite Number MCP Server")

class ToolInvocation(BaseModel):
    tool: str
    args: dict | None = None

@app.get("/handshake")
def handshake():
    return {
        "name": "FavoriteNumberServer",
        "mcp_version": "0.1",
        "tools": [
            {
                "name": "favorite_number",
                "description": "Return Lauren's favorite number",
                "parameters": {}
            }
        ]
    }

@app.post("/execute")
def execute(invocation: ToolInvocation):
    if invocation.tool == "favorite_number":
        return {"result": "Lauren's favorite number is 13"}
    return {"error": "Unknown tool"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
