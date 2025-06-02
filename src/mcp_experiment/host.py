import chainlit as cl
from mcp import ClientSession

@cl.on_chat_start
async def on_chat_start():
    # Initialize user session state
    cl.user_session.set("mcp_tools", {})

@cl.on_mcp_connect
async def on_mcp_connect(connection, session: ClientSession):
    # Fetch available tools from the MCP server
    result = await session.list_tools()
    tools = [{
        "name": t.name,
        "description": t.description,
        "parameters": t.inputSchema,
    } for t in result.tools]

    # Store tools in user session
    mcp_tools = cl.user_session.get("mcp_tools", {})
    mcp_tools[connection.name] = tools
    cl.user_session.set("mcp_tools", mcp_tools)
    pass

@cl.step(type="tool") 
async def call_tool(tool_use):
    tool_name = tool_use.name
    tool_input = tool_use.input
    
    mcp_name = tool_use.mcp_name
    
    # Get the MCP session
    mcp_session, _ = cl.context.session.mcp_sessions.get(mcp_name)
    
    # Call the tool
    result = await mcp_session.call_tool(tool_name, tool_input)
    
    return result

@cl.on_message
async def on_message(message: cl.Message):
    # Retrieve tools from user session
    mcp_tools = cl.user_session.get("mcp_tools", {})
    tools = [tool for tools_list in mcp_tools.values() for tool in tools_list]
    tools = [{"type": "function", "function": tool} for tool in tools]

    # Initialize message for streaming response
    msg = cl.Message(content="")
    await msg.send()

    # Here, you would integrate with your LLM, passing the tools as needed
    # For demonstration, we'll echo the user's message
    response = f"You said: {message.content}"
    await msg.update(content=response)