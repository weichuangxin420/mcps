from fastmcp import FastMCP
from logger import get_logger

# 获取日志记录器
logger = get_logger("mcps-server")

mcp = FastMCP("mcps-demo")

@mcp.tool
def ping(name: str = "world") -> str:
    """Return a simple greeting for smoke testing MCP server.

    Args:
        name: The name to greet.
    Returns:
        A greeting string.
    """
    logger.info(f"🔔 PING 请求收到 - 参数: name={name}")
    
    result = f"Hello, {name}!"
    logger.info(f"✅ PING 响应发送 - 结果: {result}")
    
    return result


if __name__ == "__main__":
    # Default transport is STDIO; suitable for local MCP hosts (e.g., Claude Desktop / Cursor)
    logger.info("🚀 MCP 服务器启动中...")
    
    # 添加健康检查端点
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check():
        logger.info("🏥 健康检查请求")
        return {"status": "healthy", "service": "mcps-demo", "port": 3002}
    
    mcp.run() 