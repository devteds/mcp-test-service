"""Tests for the Product Search MCP server."""

import pytest
from fastapi.testclient import TestClient

from mcp_service.server import create_app


@pytest.fixture
def client():
    """Create a test client."""
    app = create_app()
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product Search MCP Service is running"
    assert data["version"] == "0.1.0"
    assert data["service"] == "Product Search MCP Service"
    assert "endpoints" in data


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "product-search-mcp-service"
    assert data["version"] == "0.1.0"


def test_capabilities_endpoint(client):
    """Test the capabilities endpoint."""
    response = client.get("/api/v1/mcp/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert "capabilities" in data
    assert "version" in data
    assert data["service"] == "Product Search MCP Service"
    assert "available_categories" in data
