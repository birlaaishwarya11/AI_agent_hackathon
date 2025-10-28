#!/usr/bin/env python3
"""
Setup script for LinkedIn Job Applier MCP Server
Helps users configure their environment quickly
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("LinkedIn Job Applier MCP Server - Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True

def check_uv_installed():
    """Check if uv is installed"""
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ uv installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ uv package manager not found")
    print("   Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
    print("   Or: pip install uv")
    return False

def check_docker_installed():
    """Check if Docker is installed"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Docker installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  Docker not found (optional for local development)")
    print("   Install from: https://docs.docker.com/get-docker/")
    return False

def setup_environment():
    """Setup environment file"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print("✓ .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✓ Created .env file from template")
        print("   Please edit .env with your credentials")
        return True
    else:
        print("❌ .env.example not found")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        # Try uv first
        result = subprocess.run(['uv', 'sync'], check=True)
        print("✓ Dependencies installed with uv")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Fallback to pip
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', '.'], check=True)
            print("✓ Dependencies installed with pip")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False

def setup_sample_data():
    """Setup sample data files"""
    data_dir = Path('data')
    
    # Create sample resume if none exists
    resume_files = list(data_dir.glob('resume.*'))
    if not resume_files:
        sample_resume = data_dir / 'sample_resume.txt'
        sample_resume.write_text("""
John Doe
Software Engineer

EXPERIENCE:
- 5 years of Python development
- Experience with web frameworks (Django, Flask)
- Database design and optimization
- API development and integration

SKILLS:
- Python, JavaScript, SQL
- Docker, Kubernetes
- AWS, GCP
- Git, CI/CD

EDUCATION:
- Bachelor's in Computer Science
""".strip())
        print("✓ Created sample resume (data/sample_resume.txt)")
        print("   Replace with your actual resume")
    
    # Create sample cover letter template
    cover_letter = data_dir / 'cover_letter_template.txt'
    if not cover_letter.exists():
        cover_letter.write_text("""
Dear Hiring Manager,

I am excited to apply for the {job_title} position at {company_name}. 
With my background in {relevant_skills}, I believe I would be a great fit for this role.

{personalized_content}

I look forward to discussing how my experience can contribute to your team.

Best regards,
{your_name}
""".strip())
        print("✓ Created cover letter template")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print("1. Edit .env file with your credentials:")
    print("   - LINKEDIN_EMAIL and LINKEDIN_PASSWORD (required)")
    print("   - OPENAI_API_KEY or ANTHROPIC_API_KEY (for resume optimization)")
    print()
    print("2. Add your resume to the data/ directory")
    print("   - Supported formats: PDF, DOCX, TXT")
    print("   - Replace data/sample_resume.txt with your actual resume")
    print()
    print("3. Run the server:")
    print("   Local MCP server:  python run_local.py mcp")
    print("   Local API server:  python run_local.py api")
    print("   Docker:           docker-compose up")
    print()
    print("4. Test the server:")
    print("   python test_fastmcp.py")
    print()
    print("5. Deploy to free platforms:")
    print("   Railway:  railway up")
    print("   Render:   Connect GitHub repo to Render")
    print("   Fly.io:   fly deploy")
    print()
    print("📚 Documentation:")
    print("   README.md - Project overview")
    print("   USAGE.md - Tool reference")
    print("   LOCAL_DEPLOYMENT.md - Local setup guide")
    print()
    print("🔗 MCP Endpoint: http://localhost:8000/mcp")
    print("🏥 Health Check: http://localhost:8000/health")

def main():
    """Main setup function"""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    uv_available = check_uv_installed()
    docker_available = check_docker_installed()
    
    print()
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("⚠️  Dependency installation failed. You may need to install manually.")
    
    # Setup sample data
    setup_sample_data()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()