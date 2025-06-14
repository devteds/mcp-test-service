"""
MCP Client Example

Demonstrates how to connect to and interact with an MCP service.
Shows both untyped and typed client usage patterns.

Author: Chandra Shettigar <chandra@devteds.com>
"""

import asyncio

import httpx
from mcp import types


class MCPProductClient:
    """A client for interacting with our Product Search MCP server."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None

    async def connect_sse(self):
        """Connect to MCP server using Server-Sent Events (SSE)."""
        # Note: This would be used if our server supported SSE transport
        # For now, we'll use HTTP requests directly
        pass

    async def discover_capabilities(self):
        """Discover what tools the MCP server provides using raw HTTP."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/mcp/message",
                json={"id": "capabilities",
                      "method": "capabilities", "params": {}},
            )
            return response.json()

    async def call_tool(self, tool_name: str, arguments: dict):
        """Call a tool on the MCP server."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/mcp/message",
                json={
                    "id": f"call_{tool_name}",
                    "method": tool_name,
                    "params": arguments,
                },
            )
            return response.json()

    async def search_products(self, query: str = "", category: str = ""):
        """Search for products."""
        result = await self.call_tool(
            "search_products", {"query": query, "category": category}
        )
        return result.get("result", {})

    async def get_product_details(self, product_id: str):
        """Get detailed information about a product."""
        result = await self.call_tool("get_product_details", {"product_id": product_id})
        return result.get("result", {})

    async def check_inventory(self, product_id: str):
        """Check inventory for a product."""
        result = await self.call_tool("check_inventory", {"product_id": product_id})
        return result.get("result", {})


async def demo_mcp_client():
    """Demonstrate using the MCP client."""
    print("🔌 MCP Client Demo")
    print("=" * 50)

    client = MCPProductClient()

    try:
        # 1. Discover capabilities
        print("\n1. 🔍 Discovering server capabilities...")
        capabilities = await client.discover_capabilities()
        if "result" in capabilities:
            tools = capabilities["result"]["capabilities"]["tools"]
            print(f"   Found {len(tools)} tools:")
            for tool in tools:
                print(f"   - {tool['name']}: {tool['description']}")

        # 2. Search for products
        print("\n2. 🛍️ Searching for electronics...")
        electronics = await client.search_products(category="Electronics")
        if "products" in electronics:
            print(f"   Found {electronics['count']} electronics:")
            for product in electronics["products"]:
                print(f"   - {product['name']}: ${product['price']}")

        # 3. Get product details
        print("\n3. 📱 Getting iPhone details...")
        iphone = await client.get_product_details("1")
        if "name" in iphone:
            print(f"   Product: {iphone['name']}")
            print(f"   Description: {iphone['description']}")
            print(f"   Price: ${iphone['price']}")
            print(f"   Stock: {iphone['stock']} units")

        # 4. Check inventory
        print("\n4. 📦 Checking Nike shoes inventory...")
        inventory = await client.check_inventory("3")
        if "product_name" in inventory:
            print(f"   Product: {inventory['product_name']}")
            print(f"   Stock: {inventory['stock']} units")
            status = "Yes" if inventory["in_stock"] else "No"
            print(f"   Available: {status}")

        print("\n✅ Demo completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure the MCP server is running on http://localhost:8000")


# Alternative approach using the official MCP types
class TypedMCPClient:
    """Example using official MCP types for better type safety."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    async def call_tool_typed(self, request: types.CallToolRequest):
        """Call a tool using official MCP types."""
        async with httpx.AsyncClient() as client:
            # Convert MCP request to our server's format
            response = await client.post(
                f"{self.base_url}/api/v1/mcp/message",
                json={
                    "id": "typed_call",
                    "method": request.params.name,
                    "params": request.params.arguments or {},
                },
            )
            return response.json()

    async def search_products_typed(self, query: str = "", category: str = ""):
        """Search products using typed request."""
        request = types.CallToolRequest(
            method="tools/call",
            params=types.CallToolRequestParams(
                name="search_products", arguments={"query": query, "category": category}
            ),
        )
        return await self.call_tool_typed(request)


async def demo_typed_client():
    """Demonstrate using typed MCP client."""
    print("\n" + "=" * 50)
    print("🎯 Typed MCP Client Demo")
    print("=" * 50)

    client = TypedMCPClient()

    try:
        # Search using typed request
        print("\n🔍 Searching for 'iPhone' using typed client...")
        result = await client.search_products_typed(query="iPhone")

        if "result" in result and "products" in result["result"]:
            products = result["result"]["products"]
            print(f"   Found {len(products)} products:")
            for product in products:
                print(f"   - {product['name']}: ${product['price']}")

        print("\n✅ Typed demo completed!")

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    print("Starting MCP Client Examples...")
    print("Make sure your MCP server is running: python -m mcp_service")
    print()

    # Run both demos
    asyncio.run(demo_mcp_client())
    asyncio.run(demo_typed_client())
