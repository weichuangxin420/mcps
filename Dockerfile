FROM python:3.11-slim

WORKDIR /app

# Install runtime deps first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY server.py ./

# Configure defaults for HTTP transport
ENV MCP_TRANSPORT=http \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=3002 \
    MCP_PATH=/mcp

EXPOSE 3002

# Run the server via HTTP transport without modifying server.py
CMD ["python", "-c", "import os; host=os.getenv('MCP_HOST','0.0.0.0'); port=int(os.getenv('MCP_PORT','3002')); path=os.getenv('MCP_PATH','/mcp'); transport=os.getenv('MCP_TRANSPORT','http'); from server import mcp; mcp.run(transport=transport, host=host, port=port, path=path)"] 