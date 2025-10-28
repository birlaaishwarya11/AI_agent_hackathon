# Claude Desktop Setup Guide
## LinkedIn Job Applier MCP Server Integration

## 🎯 Quick Setup

### Step 1: Generate Configuration
```bash
# Run the configuration generator
python generate_claude_config.py
```

This will create a `claude_desktop_config.json` file with the correct paths and settings for your system.

### Step 2: Locate Claude Desktop Config File

The configuration file location depends on your operating system:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Step 3: Update Configuration

**Option A: Automatic (Recommended)**
```bash
python generate_claude_config.py
# Choose 'y' when prompted to copy automatically
```

**Option B: Manual Copy**
```bash
# Copy the generated config
cp claude_desktop_config.json ~/.config/Claude/claude_desktop_config.json
```

**Option C: Manual Edit**
Open your Claude Desktop config file and add this configuration:

```json
{
  "mcpServers": {
    "linkedin-job-applier": {
      "command": "python",
      "args": ["/absolute/path/to/your/project/run_local.py", "mcp"],
      "env": {
        "LINKEDIN_EMAIL": "your.email@example.com",
        "LINKEDIN_PASSWORD": "your_linkedin_password",
        "OPENAI_API_KEY": "sk-your-openai-api-key-here",
        "ANTHROPIC_API_KEY": "your-anthropic-api-key-here",
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "DEBUG": "false",
        "HEADLESS_BROWSER": "true",
        "CHROME_NO_SANDBOX": "true",
        "CHROME_DISABLE_DEV_SHM_USAGE": "true",
        "MAX_APPLICATIONS_PER_DAY": "10",
        "REQUEST_DELAY_MIN": "2",
        "REQUEST_DELAY_MAX": "5",
        "DATA_DIR": "/absolute/path/to/your/project/data",
        "LOGS_DIR": "/absolute/path/to/your/project/logs",
        "PYTHONPATH": "/absolute/path/to/your/project/src"
      }
    }
  }
}
```

## 🔧 Configuration Details

### Required Environment Variables

**LinkedIn Credentials (Required):**
```json
"LINKEDIN_EMAIL": "your.email@example.com",
"LINKEDIN_PASSWORD": "your_linkedin_password"
```

**AI API Keys (At least one required):**
```json
"OPENAI_API_KEY": "sk-your-openai-api-key-here",
"ANTHROPIC_API_KEY": "your-anthropic-api-key-here"
```

### Important Path Updates

**Replace these paths with your actual project location:**
- `/absolute/path/to/your/project/run_local.py` → Your actual project path
- `/absolute/path/to/your/project/data` → Your actual data directory
- `/absolute/path/to/your/project/logs` → Your actual logs directory
- `/absolute/path/to/your/project/src` → Your actual src directory

**Example for macOS/Linux:**
```json
"command": "python",
"args": ["/Users/yourname/linkedin-job-applier-mcp/run_local.py", "mcp"],
"env": {
  "DATA_DIR": "/Users/yourname/linkedin-job-applier-mcp/data",
  "LOGS_DIR": "/Users/yourname/linkedin-job-applier-mcp/logs",
  "PYTHONPATH": "/Users/yourname/linkedin-job-applier-mcp/src"
}
```

**Example for Windows:**
```json
"command": "python",
"args": ["C:\\Users\\yourname\\linkedin-job-applier-mcp\\run_local.py", "mcp"],
"env": {
  "DATA_DIR": "C:\\Users\\yourname\\linkedin-job-applier-mcp\\data",
  "LOGS_DIR": "C:\\Users\\yourname\\linkedin-job-applier-mcp\\logs",
  "PYTHONPATH": "C:\\Users\\yourname\\linkedin-job-applier-mcp\\src"
}
```

## 🚀 Testing the Setup

### Step 1: Restart Claude Desktop
Close and reopen Claude Desktop after updating the configuration.

### Step 2: Test MCP Connection
In Claude Desktop, try these commands:

```
Search for Python developer jobs in San Francisco
```

```
Analyze this job description: [paste job description]
```

```
What's my current application status?
```

### Step 3: Verify Tools are Available
Ask Claude:
```
What LinkedIn job tools do you have available?
```

You should see these 8 tools:
1. `search_linkedin_jobs`
2. `analyze_job_description`
3. `match_resume_to_job`
4. `optimize_resume`
5. `apply_to_job`
6. `get_application_status`
7. `manage_user_data`
8. `get_job_insights`

## 🔍 Troubleshooting

### Issue 1: "Server not found" or "Connection failed"

**Check paths:**
```bash
# Verify your project path
pwd
# Should show your project directory

# Verify run_local.py exists
ls -la run_local.py
```

**Update config with correct absolute paths:**
```bash
# Get absolute path
pwd
# Copy this path and update your claude_desktop_config.json
```

### Issue 2: "Python command not found"

**Find your Python path:**
```bash
which python
# or
which python3
```

**Update the command in config:**
```json
"command": "/usr/bin/python3",  // Use the actual path
```

### Issue 3: "Module not found" errors

**Check PYTHONPATH:**
```json
"env": {
  "PYTHONPATH": "/absolute/path/to/your/project/src"
}
```

**Verify dependencies:**
```bash
python -c "import fastmcp; print('FastMCP OK')"
python -c "from linkedin_job_applier.fastmcp_server import mcp; print('Server OK')"
```

### Issue 4: LinkedIn credentials not working

**Test credentials separately:**
```bash
# Test the server directly
python run_local.py mcp
```

**Check .env file:**
```bash
cat .env
# Verify LINKEDIN_EMAIL and LINKEDIN_PASSWORD are set
```

### Issue 5: Chrome/Browser issues

**Add browser settings to config:**
```json
"env": {
  "HEADLESS_BROWSER": "true",
  "CHROME_NO_SANDBOX": "true",
  "CHROME_DISABLE_DEV_SHM_USAGE": "true"
}
```

## 📊 Usage Examples in Claude Desktop

### Job Search
```
Search for "senior python developer" jobs in "New York" with a maximum of 10 results
```

### Resume Analysis
```
Analyze my resume against this job description: [paste job description]
```

### Resume Optimization
```
Optimize my resume for this job posting: [paste job URL or description]
```

### Job Application
```
Apply to this job: https://linkedin.com/jobs/view/123456789
```

### Application Tracking
```
What's the status of my recent job applications?
```

### Job Market Insights
```
Give me insights about the Python developer job market in San Francisco
```

## 🔐 Security Notes

### Credential Management
- Never commit your actual credentials to version control
- Use environment variables or the .env file for sensitive data
- Consider using a separate LinkedIn account for automation

### Rate Limiting
The server includes built-in rate limiting to avoid LinkedIn detection:
- `REQUEST_DELAY_MIN`: Minimum delay between requests (default: 2 seconds)
- `REQUEST_DELAY_MAX`: Maximum delay between requests (default: 5 seconds)
- `MAX_APPLICATIONS_PER_DAY`: Daily application limit (default: 10)

## 📝 Configuration Template

Here's a complete template you can customize:

```json
{
  "mcpServers": {
    "linkedin-job-applier": {
      "command": "python",
      "args": ["/YOUR/PROJECT/PATH/run_local.py", "mcp"],
      "env": {
        "LINKEDIN_EMAIL": "your.email@example.com",
        "LINKEDIN_PASSWORD": "your_password",
        "OPENAI_API_KEY": "sk-your-key",
        "ANTHROPIC_API_KEY": "your-key",
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "DEBUG": "false",
        "HEADLESS_BROWSER": "true",
        "CHROME_NO_SANDBOX": "true",
        "CHROME_DISABLE_DEV_SHM_USAGE": "true",
        "MAX_APPLICATIONS_PER_DAY": "10",
        "REQUEST_DELAY_MIN": "2",
        "REQUEST_DELAY_MAX": "5",
        "MINIMUM_MATCH_SCORE": "0.7",
        "JOB_SEARCH_KEYWORDS": "python,developer,remote",
        "PREFERRED_LOCATIONS": "San Francisco,New York,Remote",
        "DATA_DIR": "/YOUR/PROJECT/PATH/data",
        "LOGS_DIR": "/YOUR/PROJECT/PATH/logs",
        "PYTHONPATH": "/YOUR/PROJECT/PATH/src"
      }
    }
  }
}
```

## ✅ Success Checklist

- [ ] Generated configuration with `python generate_claude_config.py`
- [ ] Updated paths to match your system
- [ ] Added real LinkedIn credentials
- [ ] Added AI API key (OpenAI or Anthropic)
- [ ] Copied config to Claude Desktop location
- [ ] Restarted Claude Desktop
- [ ] Tested with a simple job search
- [ ] Verified all 8 tools are available

## 🎉 You're Ready!

Once everything is set up, you can use Claude Desktop to:
- 🔍 Search LinkedIn jobs with natural language
- 📄 Analyze and optimize your resume
- 🤖 Apply to jobs automatically
- 📊 Track your applications
- 🎯 Get job market insights

**Happy job hunting with Claude Desktop! 🚀**