"""Product database for the MCP service."""

# Our fake product database
PRODUCTS = [
    {
        "id": "1",
        "name": "iPhone 15 Pro",
        "category": "Electronics",
        "price": 999.99,
        "stock": 50,
        "description": "Latest iPhone with titanium design",
    },
    {
        "id": "2",
        "name": "MacBook Air M3",
        "category": "Electronics",
        "price": 1299.99,
        "stock": 25,
        "description": "Lightweight laptop with M3 chip",
    },
    {
        "id": "3",
        "name": "Nike Air Max",
        "category": "Footwear",
        "price": 129.99,
        "stock": 100,
        "description": "Classic running shoes",
    },
    {
        "id": "4",
        "name": "Coffee Maker Pro",
        "category": "Appliances",
        "price": 199.99,
        "stock": 15,
        "description": "Professional grade coffee maker",
    },
]


def search_products(query: str = "", category: str = "") -> list:
    """Search for products by name or category"""
    results = []

    for product in PRODUCTS:
        # Search by name or category
        name_match = query.lower() in product["name"].lower() if query else True
        category_match = (
            category.lower() == product["category"].lower() if category else True
        )

        if name_match and category_match:
            results.append(
                {
                    "id": product["id"],
                    "name": product["name"],
                    "category": product["category"],
                    "price": product["price"],
                }
            )

    return results


def get_product_details(product_id: str) -> dict:
    """Get detailed information about a specific product"""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product

    return {"error": "Product not found"}


def check_inventory(product_id: str) -> dict:
    """Check stock levels for a product"""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return {
                "product_id": product_id,
                "product_name": product["name"],
                "stock": product["stock"],
                "in_stock": product["stock"] > 0,
            }

    return {"error": "Product not found"}


def get_all_categories() -> list:
    """Get all available product categories"""
    categories = set()
    for product in PRODUCTS:
        categories.add(product["category"])
    return sorted(list(categories))
