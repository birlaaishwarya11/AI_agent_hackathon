# LinkedIn Job Applier MCP Server

🚀 **An intelligent MCP (Model Context Protocol) server that automates LinkedIn job applications with AI-powered resume optimization.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🔍 **Smart Job Discovery**: Automatically searches LinkedIn for relevant job openings from the past month
- 🎯 **Intelligent Matching**: Advanced algorithm analyzes job descriptions and matches them with your resume (74.2% match in demo!)
- 🤖 **AI Resume Optimization**: Generates tailored resume versions using GPT-4 or Claude for each job application
- 📝 **Automated Applications**: Applies to jobs automatically with optimized resumes using LinkedIn Easy Apply
- 💾 **Smart Data Management**: Stores user preferences and learns from your application history
- 📊 **Application Tracking**: Monitors success rates, provides insights, and prevents over-application
- 🛡️ **Privacy First**: All data stored locally, no cloud dependencies for personal information
- 🔧 **Highly Configurable**: Extensive customization options for matching thresholds, application limits, and more

## 🚀 Quick Start

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
MINIMUM_MATCH_SCORE=0.7
```

### 3. Add Your Resume

Place your resume in the `data/` directory. Supports PDF, DOCX, and TXT formats.

### 4. Try the Demo

```bash
python demo.py
```

This demonstrates all features with a sample resume and job description.

### 5. Start the MCP Server

```bash
linkedin-job-applier
```

## 🛠️ MCP Tools

The server exposes 8 powerful tools:

| Tool | Description | Use Case |
|------|-------------|----------|
| `search_linkedin_jobs` | Find relevant job postings | Discover opportunities matching your skills |
| `analyze_resume` | Extract skills and keywords | Understand your resume's strengths |
| `match_job_resume` | Calculate compatibility scores | Identify best-fit opportunities |
| `optimize_resume` | AI-powered resume tailoring | Increase application success rates |
| `apply_to_job` | Automated job applications | Apply efficiently with optimized resumes |
| `update_user_info` | Manage personal information | Keep application data current |
| `get_application_status` | Track application history | Monitor your job search progress |
| `get_user_info` | Retrieve stored information | Review your profile and preferences |

## 📊 Demo Results

Our demo shows impressive results:

```
✅ Resume Analysis Results:
   Technical skills found: 31
   Experience years: 5
   Top keywords: python, technology, aws, engineer, postgresql

✅ Job Matching Results:
   Overall match score: 74.2%
   Technical skills match: 100.0%
   Experience match: 100.0%
   Recommendation: Recommended - Good match with minor gaps
```

## 🏗️ Architecture

The system is built with a modular architecture:

- **MCP Server**: Handles client communication and tool orchestration
- **Job Scraper**: LinkedIn automation with anti-detection measures
- **Resume Analyzer**: NLP-powered skill and keyword extraction
- **Job Matcher**: Multi-dimensional compatibility scoring algorithm
- **Resume Optimizer**: AI-powered resume tailoring (GPT-4/Claude)
- **Job Applier**: Automated application with form filling
- **User Manager**: Personal information and preference management
- **Config Manager**: Centralized configuration and validation

## 🔒 Security & Privacy

- **Local Storage**: All personal data stored on your machine
- **No Cloud Dependencies**: Resume content never leaves your system
- **Secure Credentials**: Environment-based credential management
- **Rate Limiting**: Prevents detection and respects platform limits
- **Anti-Detection**: Advanced browser automation with human-like patterns

## 📈 Intelligent Features

### Resume-Job Matching Algorithm

Our sophisticated matching algorithm considers:
- **Technical Skills** (30% weight): Programming languages, frameworks, tools
- **Experience Level** (25% weight): Years of experience and seniority
- **Keywords** (15% weight): TF-IDF similarity between resume and job description
- **Must-Have Requirements** (15% weight): Critical job requirements
- **Soft Skills** (15% weight): Leadership, communication, teamwork

### AI-Powered Resume Optimization

Three optimization levels:
- **Light**: Summary and skills sections
- **Moderate**: Summary, skills, and experience
- **Aggressive**: All sections including projects and education

### Smart Application Management

- Daily application limits to avoid spam detection
- Match score thresholds for quality applications
- Application history tracking and analytics
- Automatic retry mechanisms for failed applications

## 📚 Documentation

- **[Usage Guide](USAGE.md)**: Comprehensive tool reference and examples
- **[Architecture](ARCHITECTURE.md)**: Detailed system design and data flow
- **[Demo Script](demo.py)**: Working examples of all features

## 🔧 Configuration Options

Extensive customization through environment variables:

```env
# Application Behavior
MAX_APPLICATIONS_PER_DAY=10
MINIMUM_MATCH_SCORE=0.7
JOB_SEARCH_KEYWORDS=software engineer,python developer
PREFERRED_LOCATIONS=San Francisco,New York,Remote

# Browser Settings
HEADLESS_BROWSER=true
BROWSER_TIMEOUT=30

# AI Settings
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

## 🚨 Legal & Ethical Use

⚠️ **Important**: This tool is for educational and personal use only.

- Use responsibly and comply with LinkedIn's Terms of Service
- Apply quality over quantity - don't spam applications
- Be honest in applications - the tool optimizes, doesn't fabricate
- Respect rate limits and platform policies
- Consider the impact on recruiters and hiring managers

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for:
- Code style and standards
- Testing requirements
- Documentation updates
- Feature requests and bug reports

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

Having issues? Check our troubleshooting guide:

1. **LinkedIn login fails**: Verify credentials, disable 2FA temporarily
2. **Resume analysis fails**: Check file format and path
3. **Applications fail**: Ensure user information is complete
4. **AI optimization fails**: Verify API keys and credits

For detailed troubleshooting, see [USAGE.md](USAGE.md#troubleshooting).

## 🌟 Acknowledgments

Built with:
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)
- [Selenium](https://selenium.dev/) for browser automation
- [OpenAI GPT-4](https://openai.com/) and [Anthropic Claude](https://anthropic.com/) for AI optimization
- [NLTK](https://nltk.org/) and [scikit-learn](https://scikit-learn.org/) for NLP
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing

---

**⭐ Star this repository if you find it useful!**

*Automate your job search intelligently and land your dream job faster.*