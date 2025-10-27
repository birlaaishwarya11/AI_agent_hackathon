#!/usr/bin/env python3
"""
TrueFoundry Deployment Script for LinkedIn Job Applier MCP Server
"""

import os
import sys
from pathlib import Path

try:
    from truefoundry.deploy import Build, Job, PythonBuild, Service
    from truefoundry.ml import Model
except ImportError:
    print("❌ TrueFoundry SDK not installed. Please install with: pip install truefoundry")
    sys.exit(1)

def deploy_mcp_server():
    """Deploy LinkedIn Job Applier MCP Server to TrueFoundry"""
    
    # Configuration
    workspace_fqn = os.getenv("TFY_WORKSPACE_FQN", "demo-workspace")  # Replace with your workspace
    
    print("🚀 Deploying LinkedIn Job Applier MCP Server to TrueFoundry...")
    
    # Define the service
    service = Service(
        name="linkedin-job-applier-mcp",
        image=Build(
            build_spec=PythonBuild(
                command="uv run python src/linkedin_job_applier/fastmcp_server.py",
                python_version="3.12",
                requirements_path="pyproject.toml"
            )
        ),
        ports=[{
            "port": 8000,
            "host": "0.0.0.0"
        }],
        env={
            # Environment variables - these should be set in TrueFoundry UI or via secrets
            "LINKEDIN_EMAIL": "{{ secrets.linkedin_email }}",
            "LINKEDIN_PASSWORD": "{{ secrets.linkedin_password }}",
            "OPENAI_API_KEY": "{{ secrets.openai_api_key }}",
            "ANTHROPIC_API_KEY": "{{ secrets.anthropic_api_key }}",
            "MAX_APPLICATIONS_PER_DAY": "10",
            "MINIMUM_MATCH_SCORE": "0.7",
            "HEADLESS_BROWSER": "true",
            "BROWSER_TIMEOUT": "30",
            "DATA_DIR": "/app/data",
            "RESUME_FILE": "/app/data/resume.pdf"
        },
        resources={
            "cpu_request": 1.0,
            "cpu_limit": 2.0,
            "memory_request": "2Gi",
            "memory_limit": "4Gi",
            "ephemeral_storage_request": "1Gi",
            "ephemeral_storage_limit": "2Gi"
        },
        replicas=1,
        liveness_probe={
            "path": "/health",
            "port": 8000,
            "initial_delay_seconds": 30,
            "period_seconds": 10,
            "timeout_seconds": 5,
            "failure_threshold": 3
        },
        readiness_probe={
            "path": "/health",
            "port": 8000,
            "initial_delay_seconds": 10,
            "period_seconds": 5,
            "timeout_seconds": 3,
            "failure_threshold": 3
        }
    )
    
    # Deploy the service
    try:
        deployment = service.deploy(workspace_fqn=workspace_fqn, wait=True)
        
        print("✅ Deployment successful!")
        print(f"📍 Service URL: {deployment.get_service_url()}")
        print(f"🔗 MCP Endpoint: {deployment.get_service_url()}/mcp")
        print(f"❤️  Health Check: {deployment.get_service_url()}/health")
        print(f"📊 Status: {deployment.get_service_url()}/status")
        
        return deployment
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)

def deploy_fastapi_version():
    """Deploy FastAPI version for REST API access"""
    
    workspace_fqn = os.getenv("TFY_WORKSPACE_FQN", "demo-workspace")
    
    print("🚀 Deploying LinkedIn Job Applier FastAPI Server to TrueFoundry...")
    
    # Define the FastAPI service
    service = Service(
        name="linkedin-job-applier-api",
        image=Build(
            build_spec=PythonBuild(
                command="uv run uvicorn src.linkedin_job_applier.server:app --host 0.0.0.0 --port 8000",
                python_version="3.12",
                requirements_path="pyproject.toml"
            )
        ),
        ports=[{
            "port": 8000,
            "host": "0.0.0.0"
        }],
        env={
            "LINKEDIN_EMAIL": "{{ secrets.linkedin_email }}",
            "LINKEDIN_PASSWORD": "{{ secrets.linkedin_password }}",
            "OPENAI_API_KEY": "{{ secrets.openai_api_key }}",
            "ANTHROPIC_API_KEY": "{{ secrets.anthropic_api_key }}",
            "MAX_APPLICATIONS_PER_DAY": "10",
            "MINIMUM_MATCH_SCORE": "0.7",
            "HEADLESS_BROWSER": "true",
            "BROWSER_TIMEOUT": "30",
            "DATA_DIR": "/app/data",
            "RESUME_FILE": "/app/data/resume.pdf"
        },
        resources={
            "cpu_request": 1.0,
            "cpu_limit": 2.0,
            "memory_request": "2Gi",
            "memory_limit": "4Gi",
            "ephemeral_storage_request": "1Gi",
            "ephemeral_storage_limit": "2Gi"
        },
        replicas=1,
        liveness_probe={
            "path": "/health",
            "port": 8000,
            "initial_delay_seconds": 30,
            "period_seconds": 10,
            "timeout_seconds": 5,
            "failure_threshold": 3
        }
    )
    
    try:
        deployment = service.deploy(workspace_fqn=workspace_fqn, wait=True)
        
        print("✅ FastAPI Deployment successful!")
        print(f"📍 Service URL: {deployment.get_service_url()}")
        print(f"📚 API Docs: {deployment.get_service_url()}/docs")
        print(f"❤️  Health Check: {deployment.get_service_url()}/health")
        
        return deployment
        
    except Exception as e:
        print(f"❌ FastAPI Deployment failed: {e}")
        sys.exit(1)

def main():
    """Main deployment function"""
    
    if len(sys.argv) < 2:
        print("Usage: python deploy_truefoundry.py [mcp|api|both]")
        print("  mcp  - Deploy MCP Server only")
        print("  api  - Deploy FastAPI Server only") 
        print("  both - Deploy both servers")
        sys.exit(1)
    
    deployment_type = sys.argv[1].lower()
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check environment variables
    workspace_fqn = os.getenv("TFY_WORKSPACE_FQN")
    if not workspace_fqn:
        print("⚠️  TFY_WORKSPACE_FQN not set. Using default: demo-workspace")
        print("   Set your workspace with: export TFY_WORKSPACE_FQN=your-workspace-fqn")
    
    print("🔧 Pre-deployment checklist:")
    print("   ✓ Make sure you're logged in: tfy login --host https://demo.truefoundry.cloud")
    print("   ✓ Set your secrets in TrueFoundry UI:")
    print("     - linkedin_email")
    print("     - linkedin_password") 
    print("     - openai_api_key (optional)")
    print("     - anthropic_api_key (optional)")
    print("   ✓ Upload your resume to the deployment")
    print()
    
    if deployment_type == "mcp":
        deploy_mcp_server()
    elif deployment_type == "api":
        deploy_fastapi_version()
    elif deployment_type == "both":
        deploy_mcp_server()
        print("\n" + "="*50 + "\n")
        deploy_fastapi_version()
    else:
        print("❌ Invalid deployment type. Use 'mcp', 'api', or 'both'")
        sys.exit(1)

if __name__ == "__main__":
    main()