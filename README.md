# MCP Test Service

A complete **Model Context Protocol (MCP)** implementation example featuring a product search service with both MCP and REST API endpoints.

This project demonstrates how to build, test, and deploy MCP services using modern Python development practices.

**Author:** Chandra Shettigar (chandra@devteds.com)

## 🎯 What This Project Demonstrates

- **Complete MCP Implementation** - Full JSON-RPC 2.0 protocol support
- **Multiple Interface Support** - Both MCP protocol and REST API endpoints
- **Production-Ready Code** - Comprehensive testing, formatting, and validation
- **Modern Development Environment** - VS Code/Cursor devcontainer setup
- **Real-World Example** - Product search with inventory management

## 📖 Related Blog Post

This code was written as a companion to the blog post: **[Building Your First MCP Server]** *(https://dev.to/shettigarc/building-your-first-mcp-server-53e8)*

The blog post covers the theory and best practices behind MCP service development, while this repository provides the complete working implementation.

## 🚀 Quick Start

### Prerequisites

- **VS Code** or **Cursor** editor
- **Docker** installed and running
- **Dev Containers extension** installed

### 1. Clone and Open

```bash
git clone git@github.com:devteds/mcp-test-service.git
cd mcp-test-service
```

Open in VS Code/Cursor and select **"Reopen in Container"** when prompted.

### 2. Verify Setup

```bash
python verify_setup.py
```

You should see:
```
✅ All dependencies installed and working correctly!
🚀 Your devcontainer is ready for MCP development
```

### 3. Start the MCP Service

```bash
python -m mcp_service
```

The service will start on `http://localhost:8000`

### 4. Test the Service

In a new terminal:

```bash
# Test MCP client
python mcp_client_example.py

# Run test suite
python -m pytest tests/ -v

# Test REST API
curl http://localhost:8000/api/v1/products/search?query=iPhone
```

## 🏗️ Project Structure

```
mcp-test/
├── .devcontainer/          # Development container configuration
│   ├── devcontainer.json   # VS Code/Cursor devcontainer settings
│   ├── Dockerfile          # Python development environment
│   └── bashrc              # Shell configuration with aliases
├── mcp_service/            # Main MCP service package
│   ├── __init__.py
│   ├── main.py            # FastAPI application and MCP server
│   ├── server.py          # MCP protocol implementation
│   ├── handlers.py        # MCP tool handlers
│   ├── models.py          # Pydantic data models
│   └── data.py            # Sample product database
├── tests/                  # Comprehensive test suite
│   └── test_product_service.py
├── mcp_client_example.py   # Example MCP client usage
├── verify_setup.py         # Environment verification script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Development Environment

### Devcontainer Features

The project includes a fully configured development environment with:

- **Python 3.11** with all dependencies pre-installed
- **VS Code Extensions**: Python, Black, isort, flake8, pytest
- **Automatic Formatting**: Code formatting on save
- **Port Forwarding**: MCP service accessible on port 8000
- **Shell Aliases**: Convenient commands for common tasks

### Available Commands

The devcontainer includes these helpful aliases:

```bash
mcp-start      # Start the MCP service
mcp-test       # Run the test suite
mcp-client     # Run the MCP client example
mcp-format     # Format code with black and isort
mcp-verify     # Verify environment setup
```

## 🛠️ MCP Service Details

### Available Tools

The MCP service provides three tools:

1. **`search_products`** - Search for products by name or category
2. **`get_product_details`** - Get detailed information about a specific product  
3. **`check_inventory`** - Check stock levels for a product

### Sample Data

The service includes sample products across three categories:
- **Electronics**: iPhone 15 Pro, MacBook Air M3
- **Footwear**: Nike Air Max, Adidas Ultraboost
- **Appliances**: *(expandable)*

### API Endpoints

**MCP Protocol:**
- `POST /api/v1/mcp` - Main MCP JSON-RPC endpoint

**REST API:**
- `GET /api/v1/mcp/capabilities` - Service capabilities discovery
- `GET /api/v1/products/search` - Product search
- `GET /api/v1/products/{id}` - Product details
- `GET /api/v1/products/{id}/inventory` - Inventory check
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

## 🧪 Testing

### Run All Tests

```bash
python -m pytest tests/ -v
```

### Test Coverage

The test suite covers:
- ✅ MCP protocol message handling
- ✅ All MCP tool implementations
- ✅ REST API endpoints
- ✅ Error handling and edge cases
- ✅ Data validation and serialization

### Manual Testing

```bash
# Test MCP capabilities discovery
curl http://localhost:8000/api/v1/mcp/capabilities

# Test product search
curl "http://localhost:8000/api/v1/products/search?query=iPhone"

# Test MCP client
python mcp_client_example.py
```

## 🎨 Code Quality

### Formatting and Linting

The project uses:
- **Black** for code formatting
- **isort** for import sorting  
- **flake8** for linting
- **pytest** for testing

Format code:
```bash
black . && isort .
```

### Pre-configured VS Code Settings

- Format on save enabled
- Organize imports on save
- pytest integration
- flake8 linting enabled

## 🔍 Verification and Troubleshooting

### Environment Verification

```bash
python verify_setup.py
```

This script checks:
- ✅ All required dependencies are installed
- ✅ MCP SDK functionality works
- ✅ Service imports are successful
- ✅ Data functions are operational

### Common Issues

**Port 8000 already in use:**
```bash
# Kill existing process
pkill -f "python -m mcp_service"
# Or use a different port
uvicorn mcp_service.main:app --port 8001
```

**Dependencies missing:**
```bash
# Rebuild devcontainer
# Command Palette > "Dev Containers: Rebuild Container"
```

**Tests failing:**
```bash
# Check service is running
curl http://localhost:8000/health

# Run tests with verbose output
python -m pytest tests/ -v --tb=short
```

## 📚 Learning Resources

### Understanding MCP

- **MCP Specification**: [Model Context Protocol Documentation](https://spec.modelcontextprotocol.io/)
- **MCP SDK**: [Official Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- **JSON-RPC 2.0**: [Protocol Specification](https://www.jsonrpc.org/specification)

### Key Concepts Demonstrated

1. **Protocol Implementation** - Complete JSON-RPC 2.0 MCP server
2. **Tool Registration** - Dynamic tool discovery and execution
3. **Type Safety** - Pydantic models for data validation
4. **Error Handling** - Proper MCP error responses
5. **Testing Strategy** - Comprehensive test coverage
6. **Development Workflow** - Modern Python development practices

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and ensure tests pass
4. **Format code**: `black . && isort .`
5. **Run tests**: `python -m pytest tests/ -v`
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Author**: [Chandra Shettigar](https://github.com/shettigarc) - Project creator and maintainer
- **Anthropic** for the Model Context Protocol specification
- **FastAPI** for the excellent web framework
- **Pydantic** for data validation and serialization
- **MCP Community** for tools and examples

---

**Happy MCP Development!** 🚀

For questions or issues, please open a GitHub issue or refer to the related blog post for detailed explanations. 