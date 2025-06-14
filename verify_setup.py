#!/usr/bin/env python3
"""
Verify MCP development environment setup.
Checks that all required dependencies are installed and working.
"""

import importlib
import sys
from typing import Tuple


def check_import(module_name: str, description: str = "") -> Tuple[bool, str]:
    """Check if a module can be imported."""
    try:
        importlib.import_module(module_name)
        return True, f"✅ {module_name} - {description}"
    except ImportError as e:
        return False, f"❌ {module_name} - {description} - Error: {e}"


def main():
    """Main verification function."""
    print("🔍 Verifying MCP Development Environment Setup")
    print("=" * 60)

    # Core dependencies we actually use
    dependencies = [
        ("fastapi", "Web framework for HTTP endpoints"),
        ("uvicorn", "ASGI server for FastAPI"),
        ("httpx", "HTTP client for async requests"),
        ("pydantic", "Data validation and serialization"),
        ("mcp", "Official MCP SDK"),
        ("mcp.client", "MCP client functionality"),
        ("mcp.types", "MCP type definitions"),
        ("pytest", "Testing framework"),
        ("black", "Code formatter"),
        ("isort", "Import sorter"),
        ("flake8", "Linting tool"),
    ]

    print("\n📦 Checking Core Dependencies:")
    print("-" * 40)

    all_good = True
    for module, desc in dependencies:
        success, message = check_import(module, desc)
        print(message)
        if not success:
            all_good = False

    # Test MCP functionality
    print("\n🧪 Testing MCP Functionality:")
    print("-" * 40)

    try:
        # Test MCP types
        from mcp import types

        types.CallToolRequest(
            method="tools/call",
            params=types.CallToolRequestParams(
                name="test_tool", arguments={"test": "value"}
            ),
        )
        print("✅ MCP types - Can create CallToolRequest")

        # Test our MCP service imports
        try:
            from mcp_service import data, models  # noqa: F401

            print("✅ MCP Service - Core modules import successfully")
        except ImportError as e:
            print(f"❌ MCP Service - Import error: {e}")
            all_good = False

        # Test data functions
        try:
            from mcp_service.data import search_products

            results = search_products("iPhone")
            if results:
                count = len(results)
                print(
                    f"✅ MCP Service - Data functions work " f"(found {count} products)"
                )
            else:
                print("⚠️ MCP Service - Data functions work " "but no products found")
        except Exception as e:
            print(f"❌ MCP Service - Data function error: {e}")
            all_good = False

    except ImportError as e:
        print(f"❌ MCP functionality test failed: {e}")
        all_good = False

    print("\n" + "=" * 60)
    if all_good:
        print("✅ All dependencies installed and working correctly!")
        print("🚀 Your devcontainer is ready for MCP development")
        print("\nQuick start commands:")
        print("  python -m mcp_service     # Start MCP server")
        print("  python mcp_client_example.py  # Test MCP client")
        print("  python -m pytest tests/  # Run test suite")
    else:
        print("❌ Some dependencies are missing or not working properly")
        print("🔧 Check the error messages above and install missing packages")

    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
