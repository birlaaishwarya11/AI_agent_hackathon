# TrueFoundry Deployment Guide

This guide provides step-by-step instructions for deploying the LinkedIn Job Applier MCP Server on TrueFoundry platform.

## 🚀 Quick Start

### Prerequisites

1. **TrueFoundry Account**: Sign up at [https://demo.truefoundry.cloud/](https://demo.truefoundry.cloud/)
2. **Python 3.12+**: Required for local development and deployment
3. **uv**: Fast Python package manager (installed automatically in Docker)

### Step 1: Install TrueFoundry CLI

```bash
pip install -U "truefoundry"
```

### Step 2: Login to TrueFoundry

```bash
tfy login --host "https://demo.truefoundry.cloud"
```

> **Important**: Use the demo environment URL for hackathons and testing.

### Step 3: Set Up Your Workspace

1. Go to [TrueFoundry Dashboard](https://demo.truefoundry.cloud/)
2. Create or select a workspace
3. Note your workspace FQN (Fully Qualified Name)

```bash
export TFY_WORKSPACE_FQN="your-workspace-fqn"
```

### Step 4: Configure Secrets

In the TrueFoundry UI, go to **Secrets** and add:

| Secret Name | Description | Required |
|-------------|-------------|----------|
| `linkedin_email` | Your LinkedIn email | ✅ Yes |
| `linkedin_password` | Your LinkedIn password | ✅ Yes |
| `openai_api_key` | OpenAI API key for GPT-4 | ⚠️ Optional* |
| `anthropic_api_key` | Anthropic API key for Claude | ⚠️ Optional* |

*At least one AI API key is required for resume optimization.

### Step 5: Deploy the MCP Server

```bash
# Deploy MCP Server only
python deploy_truefoundry.py mcp

# Deploy FastAPI version only
python deploy_truefoundry.py api

# Deploy both versions
python deploy_truefoundry.py both
```

## 📋 Deployment Options

### Option 1: MCP Server Deployment

The MCP server provides Model Context Protocol interface for AI assistants:

```bash
python deploy_truefoundry.py mcp
```

**Features:**
- Compatible with Claude, ChatGPT, and other MCP clients
- Exposes 8 powerful tools for job automation
- HTTP transport for web accessibility
- Health monitoring and status endpoints

**Endpoints:**
- MCP Interface: `https://your-service-url/mcp`
- Health Check: `https://your-service-url/health`
- Status: `https://your-service-url/status`

### Option 2: FastAPI Server Deployment

Traditional REST API for web applications:

```bash
python deploy_truefoundry.py api
```

**Features:**
- RESTful API endpoints
- Interactive API documentation
- Direct HTTP integration
- Swagger UI for testing

**Endpoints:**
- API Docs: `https://your-service-url/docs`
- Health Check: `https://your-service-url/health`

## 🔧 Configuration

### Environment Variables

The deployment automatically configures these environment variables:

```env
# LinkedIn Credentials (from secrets)
LINKEDIN_EMAIL={{ secrets.linkedin_email }}
LINKEDIN_PASSWORD={{ secrets.linkedin_password }}

# AI API Keys (from secrets)
OPENAI_API_KEY={{ secrets.openai_api_key }}
ANTHROPIC_API_KEY={{ secrets.anthropic_api_key }}

# Application Settings
MAX_APPLICATIONS_PER_DAY=10
MINIMUM_MATCH_SCORE=0.7
HEADLESS_BROWSER=true
BROWSER_TIMEOUT=30

# Storage Settings
DATA_DIR=/app/data
RESUME_FILE=/app/data/resume.pdf
```

### Resource Allocation

Default resource configuration:

```yaml
resources:
  cpu_request: 1.0 cores
  cpu_limit: 2.0 cores
  memory_request: 2Gi
  memory_limit: 4Gi
  ephemeral_storage_request: 1Gi
  ephemeral_storage_limit: 2Gi
```

### Health Checks

Both liveness and readiness probes are configured:

```yaml
liveness_probe:
  path: /health
  port: 8000
  initial_delay_seconds: 30
  period_seconds: 10

readiness_probe:
  path: /health
  port: 8000
  initial_delay_seconds: 10
  period_seconds: 5
```

## 📁 File Upload

### Resume Upload

After deployment, upload your resume file:

1. **Via TrueFoundry UI:**
   - Go to your service in the dashboard
   - Use the file upload feature to add your resume
   - Place it at `/app/data/resume.pdf` (or update `RESUME_FILE` env var)

2. **Via API (if deployed):**
   ```bash
   curl -X POST "https://your-service-url/upload-resume" \
        -F "file=@your-resume.pdf"
   ```

### Supported Resume Formats

- PDF (.pdf) - Recommended
- Microsoft Word (.docx, .doc)
- Plain Text (.txt)

## 🛠️ Advanced Configuration

### Custom Deployment Script

You can customize the deployment by modifying `deploy_truefoundry.py`:

```python
# Custom resource allocation
resources={
    "cpu_request": 2.0,      # Increase for better performance
    "cpu_limit": 4.0,
    "memory_request": "4Gi",  # Increase for large resume processing
    "memory_limit": "8Gi",
}

# Custom environment variables
env={
    "MAX_APPLICATIONS_PER_DAY": "20",  # Increase application limit
    "MINIMUM_MATCH_SCORE": "0.8",     # Higher quality threshold
    "JOB_SEARCH_KEYWORDS": "senior python developer,machine learning engineer",
    "PREFERRED_LOCATIONS": "Remote,San Francisco,New York"
}
```

### Multiple Environments

Deploy to different environments:

```bash
# Development
export TFY_WORKSPACE_FQN="dev-workspace"
python deploy_truefoundry.py mcp

# Production
export TFY_WORKSPACE_FQN="prod-workspace"
python deploy_truefoundry.py mcp
```

## 🔍 Monitoring and Debugging

### Health Monitoring

Check service health:

```bash
curl https://your-service-url/health
```

Expected response:
```json
{
  "status": "OK",
  "name": "linkedin_job_applier",
  "version": "1.0.0",
  "components": {
    "config": true,
    "job_scraper": true,
    "resume_analyzer": true,
    "job_matcher": true,
    "resume_optimizer": true,
    "job_applier": true,
    "user_manager": true
  }
}
```

### Detailed Status

Get comprehensive status:

```bash
curl https://your-service-url/status
```

### Logs

View logs in TrueFoundry dashboard:

1. Go to your service
2. Click on "Logs" tab
3. Filter by log level (INFO, ERROR, etc.)

### Common Issues

1. **Service not starting:**
   - Check secrets are properly configured
   - Verify workspace FQN is correct
   - Check resource limits

2. **LinkedIn login fails:**
   - Verify credentials in secrets
   - Check if 2FA is enabled (disable temporarily)
   - Monitor rate limiting

3. **Resume analysis fails:**
   - Ensure resume file is uploaded
   - Check file format is supported
   - Verify file permissions

4. **AI optimization fails:**
   - Check API keys are valid
   - Verify API credits/quota
   - Try switching between OpenAI and Anthropic

## 🧪 Testing Your Deployment

### MCP Server Testing

1. **Using MCP Inspector:**
   ```bash
   npx @modelcontextprotocol/inspector
   # Enter your MCP endpoint: https://your-service-url/mcp
   ```

2. **Direct HTTP Testing:**
   ```bash
   # Test tool availability
   curl -X POST "https://your-service-url/mcp/tools/list"
   
   # Test job search
   curl -X POST "https://your-service-url/mcp/tools/call" \
        -H "Content-Type: application/json" \
        -d '{
          "name": "search_linkedin_jobs",
          "arguments": {
            "keywords": "python developer",
            "location": "Remote",
            "max_results": 5
          }
        }'
   ```

### FastAPI Testing

1. **Interactive Documentation:**
   - Visit `https://your-service-url/docs`
   - Test endpoints directly in the browser

2. **API Testing:**
   ```bash
   # Test job search endpoint
   curl -X POST "https://your-service-url/search-jobs" \
        -H "Content-Type: application/json" \
        -d '{
          "keywords": "python developer",
          "location": "Remote",
          "max_results": 5
        }'
   ```

## 🔄 Updates and Maintenance

### Updating the Service

1. **Code Changes:**
   ```bash
   # Make your changes
   git add .
   git commit -m "Update feature"
   
   # Redeploy
   python deploy_truefoundry.py mcp
   ```

2. **Configuration Updates:**
   - Update secrets in TrueFoundry UI
   - Modify environment variables in deployment script
   - Redeploy the service

### Scaling

Increase replicas for higher availability:

```python
# In deploy_truefoundry.py
service = Service(
    name="linkedin-job-applier-mcp",
    replicas=3,  # Increase from 1 to 3
    # ... other configuration
)
```

### Backup and Recovery

1. **Data Backup:**
   - User data is stored in `/app/data/`
   - Set up persistent volumes for data retention
   - Regular backup of application data

2. **Configuration Backup:**
   - Export secrets and environment variables
   - Version control deployment scripts
   - Document custom configurations

## 🚨 Security Best Practices

### Secrets Management

1. **Never hardcode credentials** in deployment scripts
2. **Use TrueFoundry secrets** for sensitive data
3. **Rotate credentials** regularly
4. **Monitor access logs** for suspicious activity

### Network Security

1. **Use HTTPS** for all communications
2. **Implement rate limiting** to prevent abuse
3. **Monitor API usage** for anomalies
4. **Restrict access** to internal networks when possible

### Data Privacy

1. **Store data locally** within the container
2. **Encrypt sensitive data** at rest
3. **Implement data retention** policies
4. **Comply with privacy regulations** (GDPR, CCPA)

## 📞 Support and Troubleshooting

### Getting Help

1. **TrueFoundry Documentation:** [docs.truefoundry.com](https://docs.truefoundry.com)
2. **TrueFoundry Support:** Available through the platform
3. **Project Issues:** Check the GitHub repository
4. **Community:** Join TrueFoundry Discord/Slack

### Debug Mode

Enable debug logging:

```python
# In deploy_truefoundry.py, add to env:
env={
    "LOG_LEVEL": "DEBUG",
    "PYTHONPATH": "/app/src",
    # ... other env vars
}
```

### Performance Optimization

1. **Resource Tuning:**
   - Monitor CPU and memory usage
   - Adjust resource limits based on workload
   - Use horizontal scaling for high traffic

2. **Caching:**
   - Enable job search result caching
   - Cache resume analysis results
   - Implement Redis for distributed caching

3. **Database Optimization:**
   - Consider PostgreSQL for production
   - Implement connection pooling
   - Optimize query performance

## 🎯 Production Checklist

Before going to production:

- [ ] All secrets properly configured
- [ ] Resource limits appropriate for workload
- [ ] Health checks configured and tested
- [ ] Monitoring and alerting set up
- [ ] Backup and recovery procedures in place
- [ ] Security review completed
- [ ] Load testing performed
- [ ] Documentation updated
- [ ] Team training completed
- [ ] Rollback plan prepared

---

**🎉 Congratulations!** Your LinkedIn Job Applier MCP Server is now deployed on TrueFoundry and ready to automate your job search with AI-powered resume optimization!