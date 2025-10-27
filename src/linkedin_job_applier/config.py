"""Configuration management for LinkedIn Job Applier"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import json

class Config:
    """Configuration manager for the LinkedIn Job Applier"""
    
    def __init__(self, config_file: Optional[str] = None):
        # Load environment variables
        load_dotenv()
        
        # Base directories
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = Path(os.getenv("DATA_DIR", self.project_root / "data"))
        self.config_dir = self.project_root / "config"
        self.logs_dir = self.project_root / "logs"
        
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        # LinkedIn credentials
        self.linkedin_email = os.getenv("LINKEDIN_EMAIL")
        self.linkedin_password = os.getenv("LINKEDIN_PASSWORD")
        
        # AI API keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Application settings
        self.max_applications_per_day = int(os.getenv("MAX_APPLICATIONS_PER_DAY", "10"))
        self.job_search_keywords = os.getenv("JOB_SEARCH_KEYWORDS", "").split(",")
        self.preferred_locations = os.getenv("PREFERRED_LOCATIONS", "").split(",")
        self.minimum_match_score = float(os.getenv("MINIMUM_MATCH_SCORE", "0.7"))
        
        # Browser settings
        self.headless_browser = os.getenv("HEADLESS_BROWSER", "true").lower() == "true"
        self.browser_timeout = int(os.getenv("BROWSER_TIMEOUT", "30"))
        
        # File paths
        self.resume_file = self.data_dir / os.getenv("RESUME_FILE", "resume.pdf")
        self.user_data_file = self.data_dir / "user_data.json"
        self.applications_file = self.data_dir / "applications.json"
        self.job_cache_file = self.data_dir / "job_cache.json"
        
        # Load additional config from file if provided
        if config_file:
            self.load_config_file(config_file)
    
    def load_config_file(self, config_file: str) -> None:
        """Load configuration from JSON file"""
        config_path = Path(config_file)
        if config_path.exists():
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                for key, value in config_data.items():
                    setattr(self, key, value)
    
    def save_config_file(self, config_file: str) -> None:
        """Save current configuration to JSON file"""
        config_data = {
            "max_applications_per_day": self.max_applications_per_day,
            "job_search_keywords": self.job_search_keywords,
            "preferred_locations": self.preferred_locations,
            "minimum_match_score": self.minimum_match_score,
            "headless_browser": self.headless_browser,
            "browser_timeout": self.browser_timeout,
        }
        
        config_path = Path(config_file)
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate configuration and return status"""
        issues = []
        
        # Check required credentials
        if not self.linkedin_email:
            issues.append("LinkedIn email not configured")
        if not self.linkedin_password:
            issues.append("LinkedIn password not configured")
        
        # Check AI API keys (at least one required)
        if not self.openai_api_key and not self.anthropic_api_key:
            issues.append("No AI API key configured (OpenAI or Anthropic required)")
        
        # Check resume file
        if not self.resume_file.exists():
            issues.append(f"Resume file not found: {self.resume_file}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "config": {
                "data_dir": str(self.data_dir),
                "resume_file": str(self.resume_file),
                "max_applications_per_day": self.max_applications_per_day,
                "minimum_match_score": self.minimum_match_score,
                "has_linkedin_credentials": bool(self.linkedin_email and self.linkedin_password),
                "has_openai_key": bool(self.openai_api_key),
                "has_anthropic_key": bool(self.anthropic_api_key),
            }
        }
    
    def get_browser_options(self) -> Dict[str, Any]:
        """Get browser configuration options"""
        return {
            "headless": self.headless_browser,
            "timeout": self.browser_timeout,
            "user_data_dir": str(self.data_dir / "browser_data"),
            "download_dir": str(self.data_dir / "downloads"),
        }
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI service configuration"""
        return {
            "openai_api_key": self.openai_api_key,
            "anthropic_api_key": self.anthropic_api_key,
            "preferred_model": "gpt-4" if self.openai_api_key else "claude-3-sonnet",
        }
    
    def __str__(self) -> str:
        """String representation of config (without sensitive data)"""
        return f"""LinkedIn Job Applier Configuration:
- Data Directory: {self.data_dir}
- Resume File: {self.resume_file}
- Max Applications/Day: {self.max_applications_per_day}
- Minimum Match Score: {self.minimum_match_score}
- Headless Browser: {self.headless_browser}
- LinkedIn Credentials: {'✓' if self.linkedin_email else '✗'}
- OpenAI API Key: {'✓' if self.openai_api_key else '✗'}
- Anthropic API Key: {'✓' if self.anthropic_api_key else '✗'}"""