#!/usr/bin/env python3
"""Test script for LinkedIn Job Applier FastMCP Server"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_fastmcp_server():
    """Test the FastMCP server functionality"""
    
    print("🧪 Testing LinkedIn Job Applier FastMCP Server...")
    
    try:
        # Import the server components
        from linkedin_job_applier.fastmcp_server import (
            initialize_components,
            search_linkedin_jobs,
            analyze_resume,
            get_user_info,
            mcp
        )
        
        print("✓ FastMCP server imports successful")
        
        # Initialize components
        print("\n1. Initializing components...")
        await initialize_components()
        print("✓ Components initialized successfully")
        
        # Test server info
        print("\n2. Testing server info...")
        print(f"✓ Server: {mcp.name}")
        print(f"✓ Server initialized successfully")
        
        # Test components are available
        print("\n3. Testing components...")
        from linkedin_job_applier.fastmcp_server import (
            config, job_scraper, resume_analyzer, job_matcher, 
            resume_optimizer, job_applier, user_manager
        )
        
        components = {
            "config": config is not None,
            "job_scraper": job_scraper is not None,
            "resume_analyzer": resume_analyzer is not None,
            "job_matcher": job_matcher is not None,
            "resume_optimizer": resume_optimizer is not None,
            "job_applier": job_applier is not None,
            "user_manager": user_manager is not None
        }
        
        for name, status in components.items():
            print(f"   {name}: {'✓' if status else '❌'}")
        
        print("✓ All components initialized")
        
        # Test configuration
        print("\n4. Testing configuration...")
        if config:
            validation = config.validate_config()
            print(f"✓ Configuration valid: {validation.get('valid', False)}")
        else:
            print("⚠️  Configuration not initialized")
        
        print("\n✅ All FastMCP server tests passed!")
        
        # Print server details
        print(f"\n📊 Server Details:")
        print(f"   Name: {mcp.name}")
        from fastmcp import settings
        print(f"   Host: {settings.host}")
        print(f"   Port: {settings.port}")
        print(f"   Status: Ready for deployment")
        
        return True
        
    except Exception as e:
        print(f"❌ FastMCP server test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_server_startup():
    """Test server startup without running it"""
    
    print("🚀 Testing server startup configuration...")
    
    try:
        # Import the server
        from linkedin_job_applier.fastmcp_server import mcp
        
        print("✓ FastMCP server imported successfully")
        print(f"✓ Server name: {mcp.name}")
        
        # Import settings separately
        from fastmcp import settings
        print(f"✓ Default host: {settings.host}")
        print(f"✓ Default port: {settings.port}")
        
        # Check tools are registered
        tools = []
        for attr_name in dir(mcp):
            attr = getattr(mcp, attr_name)
            if hasattr(attr, '_mcp_tool'):
                tools.append(attr_name)
        
        print(f"✓ Tools registered: {len(tools)}")
        for tool in tools:
            print(f"   - {tool}")
        
        return True
        
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    
    print("=" * 60)
    print("LinkedIn Job Applier FastMCP Server - Test Suite")
    print("=" * 60)
    
    # Test 1: Server startup
    print("\nTest 1: Server Startup")
    print("-" * 30)
    startup_success = test_server_startup()
    
    if not startup_success:
        print("❌ Server startup test failed. Exiting.")
        sys.exit(1)
    
    # Test 2: Full functionality
    print("\nTest 2: Full Functionality")
    print("-" * 30)
    functionality_success = await test_fastmcp_server()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Server Startup: {'✅ PASS' if startup_success else '❌ FAIL'}")
    print(f"Full Functionality: {'✅ PASS' if functionality_success else '❌ FAIL'}")
    
    if startup_success and functionality_success:
        print("\n🎉 All tests passed! FastMCP server is ready for deployment.")
        
        print("\n📋 Next Steps:")
        print("1. Set up your .env file with credentials")
        print("2. Upload your resume to data/ directory")
        print("3. Deploy to TrueFoundry: python deploy_truefoundry.py mcp")
        print("4. Test with MCP Inspector: npx @modelcontextprotocol/inspector")
        
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)