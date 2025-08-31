import logging
import json
from fastmcp import FastMCP

# 配置日志格式，确保在 Docker 中可见
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # 输出到 stdout，Docker 可以捕获
    ]
)
logger = logging.getLogger(__name__)

mcp = FastMCP("mcps-demo")

# 添加请求/响应日志中间件
@mcp.middleware
async def log_requests(ctx, call_next):
    """记录所有 MCP 请求和响应的中间件"""
    # 记录请求开始
    logger.info(f"📥 MCP 请求开始 - 方法: {ctx.method}")
    
    try:
        # 调用下一个处理器
        result = await call_next(ctx)
        
        # 记录成功响应
        logger.info(f"📤 MCP 响应成功 - 方法: {ctx.method}")
        return result
        
    except Exception as e:
        # 记录错误响应
        logger.error(f"❌ MCP 响应错误 - 方法: {ctx.method}, 错误: {str(e)}")
        raise


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