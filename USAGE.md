# LinkedIn Job Applier MCP Server - Usage Guide

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd linkedin-job-applier-mcp

# Install dependencies
pip install -e .
```

### 2. Configuration

Create a `.env` file with your credentials:

```env
# LinkedIn Credentials
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# AI API Keys (at least one required)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Application Settings
MAX_APPLICATIONS_PER_DAY=10
JOB_SEARCH_KEYWORDS=software engineer,python developer,data scientist
PREFERRED_LOCATIONS=San Francisco,New York,Remote
MINIMUM_MATCH_SCORE=0.7

# Browser Settings
HEADLESS_BROWSER=true
BROWSER_TIMEOUT=30

# Storage Settings
DATA_DIR=./data
RESUME_FILE=resume.pdf
```

### 3. Prepare Your Resume

Place your resume file in the `data/` directory. Supported formats:
- PDF (.pdf)
- Microsoft Word (.docx, .doc)
- Plain text (.txt)

### 4. Run the Demo

```bash
python demo.py
```

This will demonstrate all the key features without actually applying to jobs.

### 5. Start the MCP Server

```bash
linkedin-job-applier
```

The server will start and expose MCP tools for job searching and application.

## MCP Tools Reference

### search_linkedin_jobs

Search for LinkedIn job postings from the past month.

**Parameters:**
- `keywords` (required): Job search keywords (e.g., "software engineer python")
- `location` (optional): Job location (e.g., "San Francisco, CA" or "Remote")
- `max_results` (optional): Maximum number of jobs to return (default: 50)

**Example:**
```json
{
  "keywords": "senior python developer",
  "location": "Remote",
  "max_results": 25
}
```

### analyze_resume

Analyze resume and extract keywords/skills.

**Parameters:**
- `resume_path` (required): Path to resume file (PDF, DOCX, or TXT)

**Example:**
```json
{
  "resume_path": "data/my_resume.pdf"
}
```

### match_job_resume

Match job description with resume and calculate compatibility score.

**Parameters:**
- `job_id` (required): Job ID from search results
- `job_description` (required): Job description text

**Example:**
```json
{
  "job_id": "job_12345",
  "job_description": "We are looking for a Senior Python Developer..."
}
```

### optimize_resume

Generate optimized resume version for specific job.

**Parameters:**
- `job_id` (required): Job ID to optimize resume for
- `job_description` (required): Job description text
- `optimization_level` (optional): "light", "moderate", or "aggressive" (default: "moderate")

**Example:**
```json
{
  "job_id": "job_12345",
  "job_description": "We are looking for a Senior Python Developer...",
  "optimization_level": "moderate"
}
```

### apply_to_job

Apply to a job with optimized resume.

**Parameters:**
- `job_id` (required): Job ID to apply to
- `use_optimized_resume` (optional): Whether to use AI-optimized resume (default: true)
- `cover_letter` (optional): Custom cover letter text

**Example:**
```json
{
  "job_id": "job_12345",
  "use_optimized_resume": true,
  "cover_letter": "Dear Hiring Manager, I am excited to apply..."
}
```

### get_application_status

Get status of job applications.

**Parameters:**
- `days_back` (optional): Number of days to look back (default: 7)

**Example:**
```json
{
  "days_back": 30
}
```

### update_user_info

Update user information for job applications.

**Parameters:**
- `field` (required): "personal_info", "preferences", "skills", or "experience"
- `data` (required): Data object to update

**Example:**
```json
{
  "field": "personal_info",
  "data": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@email.com",
    "phone": "(555) 123-4567"
  }
}
```

### get_user_info

Get stored user information.

**Parameters:**
- `field` (optional): "personal_info", "preferences", "skills", "experience", or "all" (default: "all")

**Example:**
```json
{
  "field": "preferences"
}
```

## Workflow Examples

### Basic Job Search and Application

1. **Search for jobs:**
   ```json
   {
     "tool": "search_linkedin_jobs",
     "parameters": {
       "keywords": "python developer",
       "location": "Remote",
       "max_results": 20
     }
   }
   ```

2. **Analyze your resume:**
   ```json
   {
     "tool": "analyze_resume",
     "parameters": {
       "resume_path": "data/resume.pdf"
     }
   }
   ```

3. **Match jobs with your resume:**
   ```json
   {
     "tool": "match_job_resume",
     "parameters": {
       "job_id": "found_job_id",
       "job_description": "job description from search results"
     }
   }
   ```

4. **Optimize resume for high-match jobs:**
   ```json
   {
     "tool": "optimize_resume",
     "parameters": {
       "job_id": "found_job_id",
       "job_description": "job description",
       "optimization_level": "moderate"
     }
   }
   ```

5. **Apply to the job:**
   ```json
   {
     "tool": "apply_to_job",
     "parameters": {
       "job_id": "found_job_id",
       "use_optimized_resume": true
     }
   }
   ```

### Setting Up User Information

1. **Update personal information:**
   ```json
   {
     "tool": "update_user_info",
     "parameters": {
       "field": "personal_info",
       "data": {
         "first_name": "John",
         "last_name": "Doe",
         "email": "john.doe@email.com",
         "phone": "(555) 123-4567",
         "location": "San Francisco, CA"
       }
     }
   }
   ```

2. **Set job preferences:**
   ```json
   {
     "tool": "update_user_info",
     "parameters": {
       "field": "preferences",
       "data": {
         "work_authorization": "yes",
         "visa_sponsorship": "no",
         "willing_to_relocate": "yes",
         "remote_work": "preferred",
         "salary_expectation": "$120,000 - $150,000"
       }
     }
   }
   ```

## Configuration Options

### Application Settings

- `MAX_APPLICATIONS_PER_DAY`: Limit daily applications to avoid being flagged
- `MINIMUM_MATCH_SCORE`: Only apply to jobs above this match threshold
- `JOB_SEARCH_KEYWORDS`: Default keywords for job searches
- `PREFERRED_LOCATIONS`: Default locations to search

### Browser Settings

- `HEADLESS_BROWSER`: Run browser in headless mode (recommended: true)
- `BROWSER_TIMEOUT`: Timeout for browser operations in seconds

### AI Settings

- `OPENAI_API_KEY`: For GPT-4 powered resume optimization
- `ANTHROPIC_API_KEY`: For Claude powered resume optimization

## Data Storage

The system stores data in the following files:

- `data/user_data.json`: User personal information and preferences
- `data/job_cache.json`: Cached job search results
- `data/job_matches.json`: Job-resume match results
- `data/applications.json`: Application history
- `data/optimization_records.json`: Resume optimization history
- `data/resume_analysis.json`: Resume analysis cache
- `data/optimized_resumes/`: Generated optimized resume files

## Security and Privacy

- All data is stored locally on your machine
- LinkedIn credentials are only used for job searching and application
- AI APIs are only used for resume optimization
- No personal data is shared with third parties
- Resume content is processed securely

## Troubleshooting

### Common Issues

1. **LinkedIn login fails:**
   - Check credentials in `.env` file
   - LinkedIn may require 2FA - disable temporarily or use app password
   - Try running with `HEADLESS_BROWSER=false` to see what's happening

2. **Resume analysis fails:**
   - Ensure resume file exists in the specified path
   - Check file format is supported (PDF, DOCX, TXT)
   - Verify file is not corrupted

3. **Job application fails:**
   - Some jobs may not support "Easy Apply"
   - User information may be incomplete
   - LinkedIn may have rate limits

4. **AI optimization fails:**
   - Check API keys are valid and have credits
   - Try switching between OpenAI and Anthropic
   - Reduce optimization level to "light"

### Debug Mode

Run with debug logging:
```bash
export PYTHONPATH=/workspace/project/src
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from linkedin_job_applier.server import main
import asyncio
asyncio.run(main())
"
```

## Legal and Ethical Considerations

- Use responsibly and in compliance with LinkedIn's Terms of Service
- Don't spam applications - use quality over quantity
- Be honest in your applications - the tool optimizes but doesn't fabricate
- Respect rate limits and don't overload LinkedIn's servers
- Consider the impact on recruiters and hiring managers

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the demo script for working examples
3. Check the logs for detailed error messages
4. Ensure all dependencies are properly installed