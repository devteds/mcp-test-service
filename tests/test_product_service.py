"""Tests for the Product Search MCP service."""

import pytest
from fastapi.testclient import TestClient

from mcp_service.server import create_app


@pytest.fixture
def client():
    """Create a test client."""
    app = create_app()
    return TestClient(app)


class TestMCPEndpoints:
    """Test MCP protocol endpoints."""

    def test_ping_message(self, client):
        """Test MCP ping message."""
        response = client.post(
            "/api/v1/mcp/message",
            json={
                "id": "test-1",
                "method": "ping",
                "params": {"timestamp": "2024-01-01T00:00:00Z"},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-1"
        assert data["result"]["message"] == "pong"
        assert data["result"]["timestamp"] == "2024-01-01T00:00:00Z"

    def test_capabilities_message(self, client):
        """Test MCP capabilities message."""
        response = client.post(
            "/api/v1/mcp/message",
            json={"id": "test-2", "method": "capabilities", "params": {}},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-2"
        assert "capabilities" in data["result"]
        tools = data["result"]["capabilities"]["tools"]
        assert len(tools) == 3
        tool_names = [tool["name"] for tool in tools]
        assert "search_products" in tool_names
        assert "get_product_details" in tool_names
        assert "check_inventory" in tool_names

    def test_search_products_message(self, client):
        """Test MCP search_products message."""
        response = client.post(
            "/api/v1/mcp/message",
            json={
                "id": "test-3",
                "method": "search_products",
                "params": {"query": "iPhone"},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-3"
        assert "products" in data["result"]
        assert data["result"]["count"] == 1
        assert data["result"]["products"][0]["name"] == "iPhone 15 Pro"

    def test_search_products_by_category(self, client):
        """Test MCP search_products by category."""
        response = client.post(
            "/api/v1/mcp/message",
            json={
                "id": "test-4",
                "method": "search_products",
                "params": {"category": "Electronics"},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-4"
        assert data["result"]["count"] == 2
        product_names = [p["name"] for p in data["result"]["products"]]
        assert "iPhone 15 Pro" in product_names
        assert "MacBook Air M3" in product_names

    def test_get_product_details_message(self, client):
        """Test MCP get_product_details message."""
        response = client.post(
            "/api/v1/mcp/message",
            json={
                "id": "test-5",
                "method": "get_product_details",
                "params": {"product_id": "1"},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-5"
        product = data["result"]
        assert product["id"] == "1"
        assert product["name"] == "iPhone 15 Pro"
        assert product["price"] == 999.99
        assert product["stock"] == 50

    def test_get_product_details_not_found(self, client):
        """Test MCP get_product_details with invalid ID."""
        response = client.post(
            "/api/v1/mcp/message",
            json={
                "id": "test-6",
                "method": "get_product_details",
                "params": {"product_id": "999"},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-6"
        assert "error" in data["result"]

    def test_check_inventory_message(self, client):
        """Test MCP check_inventory message."""
        response = client.post(
            "/api/v1/mcp/message",
            json={
                "id": "test-7",
                "method": "check_inventory",
                "params": {"product_id": "3"},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-7"
        inventory = data["result"]
        assert inventory["product_id"] == "3"
        assert inventory["product_name"] == "Nike Air Max"
        assert inventory["stock"] == 100
        assert inventory["in_stock"] is True

    def test_missing_product_id_parameter(self, client):
        """Test MCP message with missing required parameter."""
        response = client.post(
            "/api/v1/mcp/message",
            json={"id": "test-8", "method": "get_product_details", "params": {}},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-8"
        assert "error" in data
        assert data["error"]["code"] == -32602

    def test_unknown_method(self, client):
        """Test MCP message with unknown method."""
        response = client.post(
            "/api/v1/mcp/message",
            json={"id": "test-9", "method": "unknown_method", "params": {}},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-9"
        assert "error" in data
        assert data["error"]["code"] == -32601


class TestRESTEndpoints:
    """Test REST API endpoints."""

    def test_search_products_api(self, client):
        """Test REST API product search."""
        response = client.get("/api/v1/products/search?query=MacBook")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "MacBook Air M3"

    def test_search_products_by_category_api(self, client):
        """Test REST API product search by category."""
        response = client.get("/api/v1/products/search?category=Footwear")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Nike Air Max"

    def test_get_product_api(self, client):
        """Test REST API get product details."""
        response = client.get("/api/v1/products/2")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "2"
        assert data["name"] == "MacBook Air M3"
        assert data["category"] == "Electronics"

    def test_get_product_not_found_api(self, client):
        """Test REST API get product with invalid ID."""
        response = client.get("/api/v1/products/999")
        assert response.status_code == 404

    def test_check_inventory_api(self, client):
        """Test REST API inventory check."""
        response = client.get("/api/v1/products/4/inventory")
        assert response.status_code == 200
        data = response.json()
        assert data["product_id"] == "4"
        assert data["product_name"] == "Coffee Maker Pro"
        assert data["stock"] == 15

    def test_get_categories_api(self, client):
        """Test REST API get categories."""
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        categories = data["categories"]
        assert "Electronics" in categories
        assert "Footwear" in categories
        assert "Appliances" in categories
