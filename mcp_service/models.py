"""Pydantic models for MCP service."""

from typing import Any, Dict, Optional, Union

from pydantic import BaseModel


class MCPRequest(BaseModel):
    """MCP request model."""

    id: Union[str, int]
    method: str
    params: Dict[str, Any] = {}


class MCPError(BaseModel):
    """MCP error model."""

    code: int
    message: str
    data: Optional[Dict[str, Any]] = None


class MCPResponse(BaseModel):
    """MCP response model."""

    id: Union[str, int]
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None


# Product-specific models
class ProductSearchRequest(BaseModel):
    """Product search request model."""

    query: Optional[str] = ""
    category: Optional[str] = ""


class ProductDetailsRequest(BaseModel):
    """Product details request model."""

    product_id: str


class InventoryCheckRequest(BaseModel):
    """Inventory check request model."""

    product_id: str


# Product-specific models for REST API responses
class Product(BaseModel):
    """Product model."""

    id: str
    name: str
    category: str
    price: float
    stock: int
    description: str


class ProductSummary(BaseModel):
    """Product summary model for search results."""

    id: str
    name: str
    category: str
    price: float


class InventoryStatus(BaseModel):
    """Inventory status model."""

    product_id: str
    product_name: str
    stock: int
    in_stock: bool
