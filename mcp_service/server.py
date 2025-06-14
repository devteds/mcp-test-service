"""FastAPI server setup for the Product Search MCP service."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mcp_service.handlers import router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Product Search MCP Service",
        description=(
            "A Model Context Protocol (MCP) service for product search "
            "and inventory management"
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(router, prefix="/api/v1")

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "Product Search MCP Service is running",
            "version": "0.1.0",
            "service": "Product Search MCP Service",
            "endpoints": {
                "mcp": "/api/v1/mcp/message",
                "capabilities": "/api/v1/mcp/capabilities",
                "docs": "/docs",
            },
        }

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": "product-search-mcp-service",
            "version": "0.1.0",
        }

    return app
