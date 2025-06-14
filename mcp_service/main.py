"""
MCP Service Main Application

FastAPI application with MCP protocol support for product search and
inventory management.

Author: Chandra Shettigar <chandra@devteds.com>
"""

import uvicorn


def main():
    """Main entry point for the MCP service."""
    # Use import string for reload to work properly
    uvicorn.run(
        "mcp_service.server:create_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
