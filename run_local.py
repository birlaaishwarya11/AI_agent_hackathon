#!/usr/bin/env python3
"""
Local runner for LinkedIn Job Applier MCP Server
Simple script to run the server locally with minimal configuration
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs/server.log', mode='a')
        ]
    )

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['LINKEDIN_EMAIL', 'LINKEDIN_PASSWORD']
    optional_vars = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY']
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        print("❌ Missing required environment variables:")
        for var in missing_required:
            print(f"   - {var}")
        print("\n💡 Please copy .env.example to .env and fill in your credentials")
        return False
    
    if len(missing_optional) == len(optional_vars):
        print("⚠️  No AI API keys found. Resume optimization will not work.")
        print("   Please add at least one of: OPENAI_API_KEY, ANTHROPIC_API_KEY")
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def run_mcp_server():
    """Run the MCP server"""
    print("🚀 Starting LinkedIn Job Applier MCP Server...")
    
    try:
        from linkedin_job_applier.fastmcp_server import mcp
        from fastmcp import settings
        
        # Configure server settings from environment
        settings.host = os.getenv('HOST', '127.0.0.1')
        settings.port = int(os.getenv('PORT', 8000))
        
        print(f"📡 Server will run on http://{settings.host}:{settings.port}")
        print(f"🔗 MCP endpoint: http://{settings.host}:{settings.port}/mcp")
        print(f"🏥 Health check: http://{settings.host}:{settings.port}/health")
        print(f"📊 Status: http://{settings.host}:{settings.port}/status")
        
        # Initialize components
        async def startup():
            from linkedin_job_applier.fastmcp_server import initialize_components
            await initialize_components()
            print("✅ All components initialized successfully")
        
        asyncio.run(startup())
        
        print("\n🎯 Ready to accept MCP connections!")
        print("💡 Connect from:")
        print("   - Claude Desktop (add to mcp_servers config)")
        print("   - MCP Inspector: npx @modelcontextprotocol/inspector")
        print("   - Custom MCP clients")
        print("\n⏹️  Press Ctrl+C to stop the server")
        
        # Run the server
        mcp.run(transport="streamable-http", stateless_http=True)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        import traceback
        traceback.print_exc()

def run_api_server():
    """Run as FastAPI server"""
    print("🚀 Starting LinkedIn Job Applier FastAPI Server...")
    
    try:
        import uvicorn
        from linkedin_job_applier.fastmcp_server import mcp
        
        host = os.getenv('HOST', '127.0.0.1')
        port = int(os.getenv('PORT', 8000))
        
        print(f"📡 Server will run on http://{host}:{port}")
        print(f"📚 API docs: http://{host}:{port}/docs")
        print(f"🏥 Health check: http://{host}:{port}/health")
        
        # Initialize components
        async def startup():
            from linkedin_job_applier.fastmcp_server import initialize_components
            await initialize_components()
            print("✅ All components initialized successfully")
        
        asyncio.run(startup())
        
        print("\n🎯 Ready to accept API requests!")
        print("⏹️  Press Ctrl+C to stop the server")
        
        # Run with uvicorn
        uvicorn.run(
            "linkedin_job_applier.fastmcp_server:mcp",
            host=host,
            port=port,
            reload=False,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main entry point"""
    print("=" * 60)
    print("LinkedIn Job Applier MCP Server - Local Runner")
    print("=" * 60)
    
    # Load environment variables
    from dotenv import load_dotenv
    if Path('.env').exists():
        load_dotenv()
        print("✓ Loaded environment variables from .env")
    else:
        print("⚠️  No .env file found. Using system environment variables.")
    
    # Setup logging
    setup_logging()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Determine server mode
    mode = sys.argv[1] if len(sys.argv) > 1 else 'mcp'
    
    if mode == 'api':
        run_api_server()
    elif mode == 'mcp':
        run_mcp_server()
    else:
        print(f"❌ Unknown mode: {mode}")
        print("Usage: python run_local.py [mcp|api]")
        print("  mcp - Run as MCP server (default)")
        print("  api - Run as FastAPI server")
        sys.exit(1)

if __name__ == "__main__":
    main()