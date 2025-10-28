#!/usr/bin/env python3
"""
Generate Claude Desktop configuration for LinkedIn Job Applier MCP Server
This script creates the correct claude_desktop_config.json for your system
"""

import json
import os
import platform
from pathlib import Path

def get_claude_config_path():
    """Get the Claude Desktop configuration file path for the current OS"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Windows":
        return Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    elif system == "Linux":
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    else:
        return Path.home() / ".claude_desktop_config.json"

def get_project_path():
    """Get the absolute path to the current project"""
    return Path(__file__).parent.absolute()

def load_env_file():
    """Load environment variables from .env file"""
    env_vars = {}
    env_file = Path(".env")
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    
    return env_vars

def generate_config():
    """Generate Claude Desktop configuration"""
    project_path = get_project_path()
    env_vars = load_env_file()
    
    # Get Python executable path
    python_path = "python"
    try:
        import sys
        python_path = sys.executable
    except:
        pass
    
    # Create configuration
    config = {
        "mcpServers": {
            "linkedin-job-applier": {
                "command": python_path,
                "args": [str(project_path / "run_local.py"), "mcp"],
                "env": {
                    # Required credentials
                    "LINKEDIN_EMAIL": env_vars.get("LINKEDIN_EMAIL", "your.email@example.com"),
                    "LINKEDIN_PASSWORD": env_vars.get("LINKEDIN_PASSWORD", "your_linkedin_password"),
                    
                    # AI API Keys (at least one required)
                    "OPENAI_API_KEY": env_vars.get("OPENAI_API_KEY", "sk-your-openai-api-key-here"),
                    "ANTHROPIC_API_KEY": env_vars.get("ANTHROPIC_API_KEY", "your-anthropic-api-key-here"),
                    
                    # Server settings
                    "HOST": env_vars.get("HOST", "127.0.0.1"),
                    "PORT": env_vars.get("PORT", "8000"),
                    "DEBUG": env_vars.get("DEBUG", "false"),
                    
                    # Browser settings
                    "HEADLESS_BROWSER": env_vars.get("HEADLESS_BROWSER", "true"),
                    "CHROME_NO_SANDBOX": env_vars.get("CHROME_NO_SANDBOX", "true"),
                    "CHROME_DISABLE_DEV_SHM_USAGE": env_vars.get("CHROME_DISABLE_DEV_SHM_USAGE", "true"),
                    
                    # Application settings
                    "MAX_APPLICATIONS_PER_DAY": env_vars.get("MAX_APPLICATIONS_PER_DAY", "10"),
                    "REQUEST_DELAY_MIN": env_vars.get("REQUEST_DELAY_MIN", "2"),
                    "REQUEST_DELAY_MAX": env_vars.get("REQUEST_DELAY_MAX", "5"),
                    "MINIMUM_MATCH_SCORE": env_vars.get("MINIMUM_MATCH_SCORE", "0.7"),
                    
                    # Paths
                    "DATA_DIR": str(project_path / "data"),
                    "LOGS_DIR": str(project_path / "logs"),
                    "PYTHONPATH": str(project_path / "src")
                }
            }
        }
    }
    
    return config

def main():
    """Main function"""
    print("=" * 60)
    print("Claude Desktop Configuration Generator")
    print("LinkedIn Job Applier MCP Server")
    print("=" * 60)
    print()
    
    # Get paths
    project_path = get_project_path()
    claude_config_path = get_claude_config_path()
    
    print(f"📁 Project path: {project_path}")
    print(f"📁 Claude config path: {claude_config_path}")
    print()
    
    # Generate configuration
    config = generate_config()
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  No .env file found. Using default values.")
        print("   Please create .env file with your credentials before using Claude Desktop.")
        print()
    else:
        print("✓ Found .env file. Using your credentials.")
        print()
    
    # Save configuration to project directory
    local_config_file = project_path / "claude_desktop_config.json"
    with open(local_config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Generated configuration: {local_config_file}")
    print()
    
    # Show configuration
    print("📋 Generated Configuration:")
    print("-" * 40)
    print(json.dumps(config, indent=2))
    print()
    
    # Instructions
    print("📝 Next Steps:")
    print("1. Copy the configuration to Claude Desktop:")
    print(f"   cp {local_config_file} {claude_config_path}")
    print()
    print("2. Or manually copy the JSON above to:")
    print(f"   {claude_config_path}")
    print()
    print("3. Make sure your .env file has the correct credentials:")
    print("   - LINKEDIN_EMAIL")
    print("   - LINKEDIN_PASSWORD") 
    print("   - OPENAI_API_KEY or ANTHROPIC_API_KEY")
    print()
    print("4. Restart Claude Desktop")
    print()
    print("5. Test the connection:")
    print("   Ask Claude: 'Search for Python developer jobs in San Francisco'")
    print()
    
    # Offer to copy automatically
    try:
        response = input("🤔 Would you like to copy the config to Claude Desktop automatically? (y/n): ")
        if response.lower() in ['y', 'yes']:
            # Create directory if it doesn't exist
            claude_config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Backup existing config if it exists
            if claude_config_path.exists():
                backup_path = claude_config_path.with_suffix('.json.backup')
                claude_config_path.rename(backup_path)
                print(f"✓ Backed up existing config to: {backup_path}")
            
            # Copy new config
            with open(claude_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ Configuration copied to Claude Desktop!")
            print("   Please restart Claude Desktop to use the MCP server.")
        else:
            print("👍 Configuration saved locally. Copy manually when ready.")
    except KeyboardInterrupt:
        print("\n👋 Configuration saved locally.")
    
    print()
    print("🎉 Setup complete! Your LinkedIn Job Applier MCP Server is ready for Claude Desktop.")

if __name__ == "__main__":
    main()