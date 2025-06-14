"""MCP message handlers and API endpoints for Product Search Service."""

from typing import List

from fastapi import APIRouter, HTTPException

from mcp_service.data import (
    check_inventory,
    get_all_categories,
    get_product_details,
    search_products,
)
from mcp_service.models import (
    InventoryStatus,
    MCPRequest,
    MCPResponse,
    Product,
    ProductSummary,
)

router = APIRouter()


@router.post("/mcp/message", response_model=MCPResponse)
async def handle_mcp_message(request: MCPRequest) -> MCPResponse:
    """Handle incoming MCP messages for product operations."""
    try:
        # Handle different MCP methods
        if request.method == "ping":
            return MCPResponse(
                id=request.id,
                result={
                    "message": "pong",
                    "timestamp": request.params.get("timestamp"),
                },
            )

        elif request.method == "capabilities":
            return MCPResponse(
                id=request.id,
                result={
                    "capabilities": {
                        "tools": [
                            {
                                "name": "search_products",
                                "description": (
                                    "Search for products by name or category"
                                ),
                                "parameters": {
                                    "query": {
                                        "type": "string",
                                        "description": (
                                            "Search query for product name"
                                        ),
                                    },
                                    "category": {
                                        "type": "string",
                                        "description": ("Product category filter"),
                                    },
                                },
                            },
                            {
                                "name": "get_product_details",
                                "description": (
                                    "Get detailed information about a "
                                    "specific product"
                                ),
                                "parameters": {
                                    "product_id": {
                                        "type": "string",
                                        "description": "Product ID",
                                        "required": True,
                                    }
                                },
                            },
                            {
                                "name": "check_inventory",
                                "description": ("Check stock levels for a product"),
                                "parameters": {
                                    "product_id": {
                                        "type": "string",
                                        "description": "Product ID",
                                        "required": True,
                                    }
                                },
                            },
                        ]
                    }
                },
            )

        elif request.method == "search_products":
            query = request.params.get("query", "")
            category = request.params.get("category", "")
            results = search_products(query, category)
            return MCPResponse(
                id=request.id, result={"products": results, "count": len(results)}
            )

        elif request.method == "get_product_details":
            product_id = request.params.get("product_id")
            if not product_id:
                return MCPResponse(
                    id=request.id,
                    error={
                        "code": -32602,
                        "message": "Missing required parameter: product_id",
                    },
                )

            product = get_product_details(product_id)
            return MCPResponse(id=request.id, result=product)

        elif request.method == "check_inventory":
            product_id = request.params.get("product_id")
            if not product_id:
                return MCPResponse(
                    id=request.id,
                    error={
                        "code": -32602,
                        "message": "Missing required parameter: product_id",
                    },
                )

            inventory = check_inventory(product_id)
            return MCPResponse(id=request.id, result=inventory)

        else:
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32601,
                    "message": f"Method not found: {request.method}",
                },
            )

    except Exception as e:
        return MCPResponse(
            id=request.id,
            error={"code": -32603, "message": f"Internal error: {str(e)}"},
        )


# REST API endpoints for direct access
@router.get("/products/search", response_model=List[ProductSummary])
async def search_products_api(query: str = "", category: str = ""):
    """REST API endpoint for product search."""
    results = search_products(query, category)
    return [ProductSummary(**product) for product in results]


@router.get("/products/{product_id}", response_model=Product)
async def get_product_api(product_id: str):
    """REST API endpoint for product details."""
    product = get_product_details(product_id)
    if "error" in product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)


@router.get("/products/{product_id}/inventory", response_model=InventoryStatus)
async def check_inventory_api(product_id: str):
    """REST API endpoint for inventory check."""
    inventory = check_inventory(product_id)
    if "error" in inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    return InventoryStatus(**inventory)


@router.get("/categories")
async def get_categories_api():
    """REST API endpoint for available categories."""
    return {"categories": get_all_categories()}


@router.get("/mcp/capabilities")
async def get_capabilities():
    """Get MCP service capabilities."""
    return {
        "service": "Product Search MCP Service",
        "version": "0.1.0",
        "capabilities": {
            "tools": [
                {
                    "name": "search_products",
                    "description": "Search for products by name or category",
                },
                {
                    "name": "get_product_details",
                    "description": (
                        "Get detailed information about a specific product"
                    ),
                },
                {
                    "name": "check_inventory",
                    "description": "Check stock levels for a product",
                },
            ]
        },
        "available_categories": get_all_categories(),
    }
