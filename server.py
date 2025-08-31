from fastmcp import FastMCP

mcp = FastMCP("mcps-demo")


@mcp.tool
def ping(name: str = "world") -> str:
    """Return a simple greeting for smoke testing MCP server.

    Args:
        name: The name to greet.
    Returns:
        A greeting string.
    """
    return f"Hello, {name}!"


if __name__ == "__main__":
    # Default transport is STDIO; suitable for local MCP hosts (e.g., Claude Desktop / Cursor)
    mcp.run() 