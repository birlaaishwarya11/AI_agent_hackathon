#!/usr/bin/env python3
"""Basic test script for LinkedIn Job Applier MCP Server"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from linkedin_job_applier.config import Config
from linkedin_job_applier.server import LinkedInJobApplierServer

async def test_basic_functionality():
    """Test basic server functionality"""
    print("Testing LinkedIn Job Applier MCP Server...")
    
    try:
        # Test configuration
        print("\n1. Testing Configuration...")
        config = Config()
        print(f"✓ Config loaded successfully")
        print(f"  Data directory: {config.data_dir}")
        print(f"  Resume file: {config.resume_file}")
        
        validation = config.validate_config()
        print(f"  Config valid: {validation['valid']}")
        if validation['issues']:
            print(f"  Issues: {validation['issues']}")
        
        # Test server initialization
        print("\n2. Testing Server Initialization...")
        server = LinkedInJobApplierServer()
        print("✓ Server created successfully")
        
        # Test tools list
        print("\n3. Testing Tools List...")
        tools = server.get_tools()
        print(f"✓ Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        print("\n✅ Basic functionality test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_basic_functionality())
    sys.exit(0 if success else 1)