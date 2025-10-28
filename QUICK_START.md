# LinkedIn Job Applier MCP Server - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Setup (30 seconds)
```bash
# Clone and setup
git clone <your-repo>
cd linkedin-job-applier-mcp
python setup.py
```

### 2. Configure (2 minutes)
```bash
# Edit .env file with your credentials
nano .env
```

**Required:**
- `LINKEDIN_EMAIL` - Your LinkedIn email
- `LINKEDIN_PASSWORD` - Your LinkedIn password
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` - For resume optimization

### 3. Add Resume (1 minute)
```bash
# Copy your resume to data directory
cp ~/my_resume.pdf data/resume.pdf
```

### 4. Run Server (30 seconds)
```bash
# MCP Server (for Claude Desktop, ChatGPT)
python run_local.py mcp

# Or FastAPI Server (REST API with docs)
python run_local.py api
```

### 5. Test (1 minute)
```bash
# Test the server
python test_fastmcp.py

# Check health
curl http://localhost:8000/health
```

## 🎯 What You Get

### MCP Tools Available:
1. **search_linkedin_jobs** - Find jobs matching your criteria
2. **analyze_job_description** - Extract requirements and skills
3. **match_resume_to_job** - Calculate compatibility score
4. **optimize_resume** - AI-powered resume enhancement
5. **apply_to_job** - Automated job application
6. **get_application_status** - Track your applications
7. **manage_user_data** - Store preferences and info
8. **get_job_insights** - Market analysis and trends

### Endpoints:
- **MCP**: `http://localhost:8000/mcp`
- **Health**: `http://localhost:8000/health`
- **API Docs**: `http://localhost:8000/docs` (API mode)
- **Status**: `http://localhost:8000/status`

## 🌐 Deployment Options

### Local Development
```bash
# MCP Server
python run_local.py mcp

# FastAPI Server
python run_local.py api

# Docker
docker-compose up
```

### Free Cloud Deployment

#### Railway (Recommended)
```bash
npm install -g @railway/cli
railway login
railway up
```

#### Render
1. Connect GitHub repo to Render
2. Select `render.yaml` configuration
3. Add environment variables

#### Fly.io
```bash
curl -L https://fly.io/install.sh | sh
fly auth login
fly deploy
```

## 🔌 Connect to MCP Clients

### Claude Desktop
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "linkedin-job-applier": {
      "command": "python",
      "args": ["/path/to/run_local.py", "mcp"],
      "env": {
        "LINKEDIN_EMAIL": "your.email@example.com",
        "LINKEDIN_PASSWORD": "your_password"
      }
    }
  }
}
```

### MCP Inspector (Testing)
```bash
npx @modelcontextprotocol/inspector
# Enter: http://localhost:8000/mcp
```

## 🛠️ Development Commands

```bash
# Setup everything
make setup

# Install dependencies
make install

# Run tests
make test

# Start MCP server
make run-mcp

# Start API server
make run-api

# Docker build and run
make docker-up

# Deploy to Railway
make railway

# Deploy to Fly.io
make fly

# Clean up
make clean
```

## 📊 Usage Examples

### Search Jobs
```python
# Via MCP client
result = await session.call_tool("search_linkedin_jobs", {
    "keywords": "python developer",
    "location": "Remote",
    "max_results": 10
})
```

### Optimize Resume
```python
# Via MCP client
result = await session.call_tool("optimize_resume", {
    "job_description": "Python developer role...",
    "optimization_level": "moderate"
})
```

### Apply to Job
```python
# Via MCP client
result = await session.call_tool("apply_to_job", {
    "job_url": "https://linkedin.com/jobs/view/123456",
    "cover_letter_template": "custom"
})
```

## 🔧 Configuration Options

### Environment Variables
```bash
# LinkedIn Credentials (Required)
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password

# AI API Keys (At least one required)
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=your-key

# Server Settings
HOST=127.0.0.1
PORT=8000
DEBUG=false

# Job Search Settings
MAX_APPLICATIONS_PER_DAY=10
JOB_SEARCH_KEYWORDS=python,developer,remote
PREFERRED_LOCATIONS=San Francisco,New York,Remote
MINIMUM_MATCH_SCORE=0.7

# Browser Settings
HEADLESS_BROWSER=true
BROWSER_TIMEOUT=30
CHROME_NO_SANDBOX=true
CHROME_DISABLE_DEV_SHM_USAGE=true

# Rate Limiting
REQUEST_DELAY_MIN=2
REQUEST_DELAY_MAX=5

# Resume Settings
RESUME_OPTIMIZATION_LEVEL=moderate
AUTO_APPLY_ENABLED=false
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Chrome/ChromeDriver Issues
```bash
# Install Chrome (Ubuntu/Debian)
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update && apt-get install -y google-chrome-stable

# Or use Docker
docker-compose up
```

#### 2. LinkedIn Detection
```bash
# Increase delays in .env
REQUEST_DELAY_MIN=5
REQUEST_DELAY_MAX=10
MAX_APPLICATIONS_PER_DAY=5
```

#### 3. Port Already in Use
```bash
# Change port
PORT=8001

# Or kill existing process
lsof -ti:8000 | xargs kill -9
```

#### 4. Missing Dependencies
```bash
# Reinstall all dependencies
pip install -e .
```

### Getting Help

1. **Check logs**: `tail -f logs/server.log`
2. **Test health**: `curl http://localhost:8000/health`
3. **Run diagnostics**: `python test_fastmcp.py`
4. **Check environment**: `python -c "import os; print(os.environ.get('LINKEDIN_EMAIL'))"`

## 📚 Documentation

- **[README.md](README.md)** - Project overview
- **[LOCAL_DEPLOYMENT.md](LOCAL_DEPLOYMENT.md)** - Detailed deployment guide
- **[USAGE.md](USAGE.md)** - Tool reference and examples
- **[QUICK_START.md](QUICK_START.md)** - This guide

## 🎉 Success!

Your LinkedIn Job Applier MCP Server is now ready to:
- 🔍 Search LinkedIn jobs automatically
- 📄 Optimize your resume for each job
- 🤖 Apply to jobs with AI assistance
- 📊 Track application status
- 🎯 Match jobs to your skills

**Happy job hunting! 🚀**

---

*Need help? Check the troubleshooting section or run `python test_fastmcp.py` for diagnostics.*