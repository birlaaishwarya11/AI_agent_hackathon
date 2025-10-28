# LinkedIn Job Applier MCP Server - Makefile

.PHONY: help setup install test run-mcp run-api docker-build docker-up clean

# Default target
help:
	@echo "LinkedIn Job Applier MCP Server"
	@echo "==============================="
	@echo ""
	@echo "Available commands:"
	@echo "  setup      - Run initial setup"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests"
	@echo "  run-mcp    - Run MCP server locally"
	@echo "  run-api    - Run FastAPI server locally"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-up  - Run with Docker Compose"
	@echo "  clean      - Clean up generated files"
	@echo ""
	@echo "Deployment:"
	@echo "  railway    - Deploy to Railway"
	@echo "  fly        - Deploy to Fly.io"
	@echo ""

# Setup
setup:
	@echo "🚀 Setting up LinkedIn Job Applier MCP Server..."
	python setup.py

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	@if command -v uv >/dev/null 2>&1; then \
		uv sync; \
	else \
		pip install -e .; \
	fi

# Run tests
test:
	@echo "🧪 Running tests..."
	python test_fastmcp.py

# Run MCP server
run-mcp:
	@echo "🚀 Starting MCP server..."
	python run_local.py mcp

# Run FastAPI server
run-api:
	@echo "🚀 Starting FastAPI server..."
	python run_local.py api

# Docker build
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t linkedin-job-applier-mcp .

# Docker compose up
docker-up:
	@echo "🐳 Starting with Docker Compose..."
	docker-compose up --build

# Railway deployment
railway:
	@echo "🚂 Deploying to Railway..."
	@if command -v railway >/dev/null 2>&1; then \
		railway up; \
	else \
		echo "❌ Railway CLI not found. Install with: npm install -g @railway/cli"; \
	fi

# Fly.io deployment
fly:
	@echo "🪰 Deploying to Fly.io..."
	@if command -v fly >/dev/null 2>&1; then \
		fly deploy; \
	else \
		echo "❌ Fly CLI not found. Install from: https://fly.io/docs/hands-on/install-flyctl/"; \
	fi

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf logs/*.log

# Development helpers
dev-setup: setup install test
	@echo "✅ Development environment ready!"

# Production check
prod-check:
	@echo "🔍 Running production checks..."
	@python -c "import os; print('✓ LINKEDIN_EMAIL set' if os.getenv('LINKEDIN_EMAIL') else '❌ LINKEDIN_EMAIL missing')"
	@python -c "import os; print('✓ LINKEDIN_PASSWORD set' if os.getenv('LINKEDIN_PASSWORD') else '❌ LINKEDIN_PASSWORD missing')"
	@python -c "import os; print('✓ AI API key set' if os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY') else '❌ No AI API key found')"
	@python test_fastmcp.py

# Show status
status:
	@echo "📊 Server Status:"
	@curl -s http://localhost:8000/health 2>/dev/null | python -m json.tool || echo "❌ Server not running"