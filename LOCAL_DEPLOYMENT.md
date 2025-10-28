# LinkedIn Job Applier MCP Server - Local & Free Deployment Guide

## 🏠 Local Development Setup

### Quick Start

1. **Clone and Setup:**
   ```bash
   git clone <your-repo>
   cd linkedin-job-applier-mcp
   python setup.py
   ```

2. **Configure Environment:**
   ```bash
   # Edit .env file with your credentials
   nano .env
   ```

3. **Run the Server:**
   ```bash
   # MCP Server (recommended)
   python run_local.py mcp
   
   # Or FastAPI Server
   python run_local.py api
   ```

4. **Test the Server:**
   ```bash
   python test_fastmcp.py
   ```

### Prerequisites

- **Python 3.8+** (required)
- **uv package manager** (recommended) or pip
- **Docker** (optional, for containerized deployment)
- **Chrome/Chromium** (for LinkedIn automation)

### Installation Options

#### Option 1: Using uv (Recommended)
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

#### Option 2: Using pip
```bash
pip install -e .
```

#### Option 3: Using Docker
```bash
docker-compose up
```

### Configuration

#### Required Environment Variables
```bash
# LinkedIn credentials
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password

# At least one AI API key for resume optimization
OPENAI_API_KEY=sk-your-openai-key
# OR
ANTHROPIC_API_KEY=your-anthropic-key
```

#### Optional Configuration
```bash
# Server settings
HOST=127.0.0.1
PORT=8000
DEBUG=false

# Job search preferences
MAX_APPLICATIONS_PER_DAY=10
JOB_SEARCH_KEYWORDS=software engineer,python developer
PREFERRED_LOCATIONS=San Francisco,New York,Remote
MINIMUM_MATCH_SCORE=0.7

# Browser settings
HEADLESS_BROWSER=true
BROWSER_TIMEOUT=30
```

### Directory Structure
```
linkedin-job-applier-mcp/
├── data/                 # Your resume and data files
│   ├── resume.pdf       # Your resume (add this)
│   └── cover_letter_template.txt
├── logs/                # Server logs
├── src/                 # Source code
├── .env                 # Your configuration (create from .env.example)
├── docker-compose.yml   # Docker setup
├── run_local.py         # Local server runner
└── setup.py            # Setup script
```

## 🌐 Free Deployment Options

### 1. Railway (Recommended)

**Pros:** Easy setup, generous free tier, automatic deployments
**Free Tier:** $5 credit monthly, 500 hours execution time

#### Setup Steps:
1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables:**
   ```bash
   railway variables set LINKEDIN_EMAIL=your.email@example.com
   railway variables set LINKEDIN_PASSWORD=your_password
   railway variables set OPENAI_API_KEY=sk-your-key
   ```

4. **Access Your Service:**
   - Railway will provide a URL like: `https://your-app.railway.app`
   - MCP endpoint: `https://your-app.railway.app/mcp`

#### Railway Configuration (railway.json):
```json
{
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "python src/linkedin_job_applier/fastmcp_server.py",
    "healthcheckPath": "/health"
  }
}
```

### 2. Render

**Pros:** Simple GitHub integration, good free tier
**Free Tier:** 750 hours/month, sleeps after 15 min inactivity

#### Setup Steps:
1. **Connect GitHub Repository:**
   - Go to [render.com](https://render.com)
   - Connect your GitHub account
   - Select your repository

2. **Configure Service:**
   - Service Type: Web Service
   - Environment: Docker
   - Build Command: (leave empty)
   - Start Command: `python src/linkedin_job_applier/fastmcp_server.py`

3. **Set Environment Variables:**
   - Add all required variables in Render dashboard
   - Mark sensitive variables as "secret"

4. **Deploy:**
   - Render will automatically deploy on git push

#### Render Configuration (render.yaml):
```yaml
services:
  - type: web
    name: linkedin-job-applier-mcp
    env: docker
    plan: free
    buildCommand: ""
    startCommand: "python src/linkedin_job_applier/fastmcp_server.py"
    healthCheckPath: /health
```

### 3. Fly.io

**Pros:** Global edge deployment, good performance
**Free Tier:** 3 shared-cpu-1x VMs, 160GB bandwidth

#### Setup Steps:
1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login and Initialize:**
   ```bash
   fly auth login
   fly launch
   ```

3. **Set Secrets:**
   ```bash
   fly secrets set LINKEDIN_EMAIL=your.email@example.com
   fly secrets set LINKEDIN_PASSWORD=your_password
   fly secrets set OPENAI_API_KEY=sk-your-key
   ```

4. **Deploy:**
   ```bash
   fly deploy
   ```

#### Fly Configuration (fly.toml):
```toml
app = "linkedin-job-applier-mcp"

[http_service]
  internal_port = 8080
  force_https = true

[[http_service.checks]]
  path = "/health"
  interval = "15s"
```

### 4. Heroku (Alternative)

**Note:** Heroku removed their free tier, but still worth mentioning for paid options.

#### Setup Steps:
1. **Install Heroku CLI and Deploy:**
   ```bash
   heroku create your-app-name
   heroku container:push web
   heroku container:release web
   ```

2. **Set Environment Variables:**
   ```bash
   heroku config:set LINKEDIN_EMAIL=your.email@example.com
   heroku config:set LINKEDIN_PASSWORD=your_password
   ```

## 🔧 Local Development Workflow

### 1. Development Mode
```bash
# Run with auto-reload for development
python run_local.py mcp
```

### 2. Testing
```bash
# Run test suite
python test_fastmcp.py

# Test specific functionality
uv run python -c "
from src.linkedin_job_applier.job_scraper import LinkedInJobScraper
scraper = LinkedInJobScraper()
print('✓ Job scraper initialized')
"
```

### 3. Docker Development
```bash
# Build and run with Docker
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Debugging
```bash
# Enable debug mode
export DEBUG=true
python run_local.py mcp

# Check logs
tail -f logs/server.log

# Test health endpoint
curl http://localhost:8000/health
```

## 🔌 Connecting MCP Clients

### Claude Desktop
Add to your `claude_desktop_config.json`:
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
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Test your server
npx @modelcontextprotocol/inspector
# Enter endpoint: http://localhost:8000/mcp
```

### Custom MCP Client
```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_client():
    server_params = StdioServerParameters(
        command="python",
        args=["run_local.py", "mcp"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools.tools]}")
            
            # Call a tool
            result = await session.call_tool("search_linkedin_jobs", {
                "keywords": "python developer",
                "location": "Remote",
                "max_results": 5
            })
            print(f"Search results: {result}")

# Run the client
asyncio.run(test_mcp_client())
```

## 📊 Monitoring and Maintenance

### Health Checks
```bash
# Check server health
curl http://localhost:8000/health

# Check detailed status
curl http://localhost:8000/status

# Check MCP endpoint
curl http://localhost:8000/mcp
```

### Log Management
```bash
# View recent logs
tail -f logs/server.log

# Rotate logs (add to crontab)
find logs/ -name "*.log" -mtime +7 -delete
```

### Performance Monitoring
```bash
# Monitor resource usage
docker stats  # if using Docker
htop          # system resources
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Chrome/ChromeDriver Issues
```bash
# Install Chrome on Ubuntu/Debian
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update && apt-get install -y google-chrome-stable

# Or use Docker (recommended for deployment)
docker-compose up
```

#### 2. LinkedIn Detection
```bash
# Increase delays in .env
REQUEST_DELAY_MIN=5
REQUEST_DELAY_MAX=10
MAX_APPLICATIONS_PER_DAY=5
```

#### 3. Memory Issues
```bash
# Reduce concurrent operations
MAX_CONCURRENT_JOBS=1
CHROME_MEMORY_LIMIT=512
```

#### 4. Port Already in Use
```bash
# Change port in .env
PORT=8001

# Or kill existing process
lsof -ti:8000 | xargs kill -9
```

### Getting Help

1. **Check logs:** `tail -f logs/server.log`
2. **Test health:** `curl http://localhost:8000/health`
3. **Run diagnostics:** `python test_fastmcp.py`
4. **Check environment:** `python -c "import os; print(os.environ.get('LINKEDIN_EMAIL'))"`

## 🎯 Production Considerations

### Security
- Use environment variables for secrets
- Enable HTTPS in production
- Implement rate limiting
- Regular security updates

### Performance
- Use Redis for caching (optional)
- Implement connection pooling
- Monitor resource usage
- Set up log rotation

### Reliability
- Implement health checks
- Set up monitoring alerts
- Use process managers (PM2, systemd)
- Regular backups of data directory

## 🎉 Success Metrics

Track your deployment success:
- **Uptime:** > 99% availability
- **Response Time:** < 2s for API calls
- **Job Processing:** 10-50 jobs per search
- **Application Success:** 70%+ for Easy Apply jobs

---

**Happy job hunting with your locally deployed MCP server! 🚀**