"""LinkedIn Job Applier FastMCP Server for TrueFoundry Deployment"""

import asyncio
import logging
import os
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from .config import Config
from .job_scraper import LinkedInJobScraper
from .resume_analyzer import ResumeAnalyzer
from .job_matcher import JobMatcher
from .resume_optimizer import ResumeOptimizer
from .job_applier import JobApplier
from .user_manager import UserManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("linkedin_job_applier")

# Global components (initialized on startup)
config: Optional[Config] = None
job_scraper: Optional[LinkedInJobScraper] = None
resume_analyzer: Optional[ResumeAnalyzer] = None
job_matcher: Optional[JobMatcher] = None
resume_optimizer: Optional[ResumeOptimizer] = None
job_applier: Optional[JobApplier] = None
user_manager: Optional[UserManager] = None

async def initialize_components():
    """Initialize all components"""
    global config, job_scraper, resume_analyzer, job_matcher, resume_optimizer, job_applier, user_manager
    
    try:
        logger.info("Initializing LinkedIn Job Applier components...")
        
        config = Config()
        job_scraper = LinkedInJobScraper(config)
        resume_analyzer = ResumeAnalyzer(config)
        job_matcher = JobMatcher(config)
        resume_optimizer = ResumeOptimizer(config)
        job_applier = JobApplier(config)
        user_manager = UserManager(config)
        
        # Initialize components that need async setup
        await user_manager.load_user_data()
        await resume_analyzer.initialize()
        
        logger.info("All components initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        raise

# --- MCP Tools ---

@mcp.tool()
def search_linkedin_jobs(keywords: str, location: str = "", max_results: int = 50) -> str:
    """
    Search for LinkedIn job postings from the past month.
    
    Args:
        keywords: Job search keywords (e.g., 'software engineer python')
        location: Job location (e.g., 'San Francisco, CA' or 'Remote')
        max_results: Maximum number of jobs to return (default: 50)
    
    Returns:
        JSON string with job search results
    """
    try:
        if not job_scraper:
            return '{"error": "Job scraper not initialized"}'
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                job_scraper.search_jobs(keywords, location, max_results)
            )
            return str(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        return f'{{"error": "Failed to search jobs: {str(e)}"}}'

@mcp.tool()
def analyze_resume(resume_path: str) -> str:
    """
    Analyze resume and extract keywords/skills.
    
    Args:
        resume_path: Path to resume file (PDF, DOCX, or TXT)
    
    Returns:
        JSON string with resume analysis results
    """
    try:
        if not resume_analyzer:
            return '{"error": "Resume analyzer not initialized"}'
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                resume_analyzer.analyze_resume(resume_path)
            )
            return str(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error analyzing resume: {e}")
        return f'{{"error": "Failed to analyze resume: {str(e)}"}}'

@mcp.tool()
def match_job_resume(job_id: str, job_description: str) -> str:
    """
    Match job description with resume and calculate compatibility score.
    
    Args:
        job_id: Job ID from search results
        job_description: Job description text
    
    Returns:
        JSON string with matching results and compatibility score
    """
    try:
        if not job_matcher:
            return '{"error": "Job matcher not initialized"}'
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                job_matcher.match_job_resume(job_id, job_description)
            )
            return str(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error matching job with resume: {e}")
        return f'{{"error": "Failed to match job with resume: {str(e)}"}}'

@mcp.tool()
def optimize_resume(job_id: str, job_description: str, optimization_level: str = "moderate") -> str:
    """
    Generate optimized resume version for specific job using AI.
    
    Args:
        job_id: Job ID to optimize resume for
        job_description: Job description text
        optimization_level: Level of optimization - 'light', 'moderate', or 'aggressive'
    
    Returns:
        JSON string with optimization results and file path
    """
    try:
        if not resume_optimizer:
            return '{"error": "Resume optimizer not initialized"}'
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                resume_optimizer.optimize_resume(job_id, job_description, optimization_level)
            )
            return str(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error optimizing resume: {e}")
        return f'{{"error": "Failed to optimize resume: {str(e)}"}}'

@mcp.tool()
def apply_to_job(job_id: str, use_optimized_resume: bool = True, cover_letter: str = "") -> str:
    """
    Apply to a job with optimized resume.
    
    Args:
        job_id: Job ID to apply to
        use_optimized_resume: Whether to use AI-optimized resume
        cover_letter: Optional custom cover letter
    
    Returns:
        JSON string with application results
    """
    try:
        if not job_applier:
            return '{"error": "Job applier not initialized"}'
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                job_applier.apply_to_job(job_id, use_optimized_resume, cover_letter)
            )
            return str(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error applying to job: {e}")
        return f'{{"error": "Failed to apply to job: {str(e)}"}}'

@mcp.tool()
def get_application_status(days_back: int = 7) -> str:
    """
    Get status of job applications.
    
    Args:
        days_back: Number of days to look back (default: 7)
    
    Returns:
        JSON string with application status and statistics
    """
    try:
        if not job_applier:
            return '{"error": "Job applier not initialized"}'
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                job_applier.get_application_status(days_back)
            )
            return str(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error getting application status: {e}")
        return f'{{"error": "Failed to get application status: {str(e)}"}}'

@mcp.tool()
def update_user_info(field: str, data: str) -> str:
    """
    Update user information for job applications.
    
    Args:
        field: Type of information - 'personal_info', 'preferences', 'skills', or 'experience'
        data: JSON string with data to update
    
    Returns:
        JSON string with update results
    """
    try:
        if not user_manager:
            return '{"error": "User manager not initialized"}'
        
        import json
        data_dict = json.loads(data)
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                user_manager.update_user_info(field, data_dict)
            )
            return str(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error updating user info: {e}")
        return f'{{"error": "Failed to update user info: {str(e)}"}}'

@mcp.tool()
def get_user_info(field: str = "all") -> str:
    """
    Get stored user information.
    
    Args:
        field: Type of information to retrieve - 'personal_info', 'preferences', 'skills', 'experience', or 'all'
    
    Returns:
        JSON string with user information
    """
    try:
        if not user_manager:
            return '{"error": "User manager not initialized"}'
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                user_manager.get_user_info(field)
            )
            return str(result)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error getting user info: {e}")
        return f'{{"error": "Failed to get user info: {str(e)}"}}'

# --- Resources ---

@mcp.resource("config://server-info")
async def get_server_info() -> dict:
    """Provides information about the LinkedIn Job Applier MCP server."""
    return {
        "server_name": mcp.name,
        "description": "AI-powered LinkedIn job application automation with resume optimization",
        "version": "1.0.0",
        "tools": [
            "search_linkedin_jobs(keywords, location, max_results) -> job search results",
            "analyze_resume(resume_path) -> resume analysis with skills and keywords",
            "match_job_resume(job_id, job_description) -> compatibility score and analysis",
            "optimize_resume(job_id, job_description, optimization_level) -> AI-optimized resume",
            "apply_to_job(job_id, use_optimized_resume, cover_letter) -> application results",
            "get_application_status(days_back) -> application history and statistics",
            "update_user_info(field, data) -> update personal information",
            "get_user_info(field) -> retrieve stored information"
        ],
        "features": [
            "LinkedIn job scraping with anti-detection",
            "NLP-powered resume analysis",
            "Multi-dimensional job matching algorithm",
            "AI resume optimization (GPT-4/Claude)",
            "Automated job applications",
            "Application tracking and analytics",
            "User data management"
        ]
    }

@mcp.resource("config://configuration")
async def get_configuration() -> dict:
    """Get current server configuration."""
    if not config:
        return {"error": "Configuration not initialized"}
    
    validation = config.validate_config()
    return {
        "valid": validation["valid"],
        "issues": validation["issues"],
        "config": validation["config"]
    }

# --- Custom Routes ---

@mcp.custom_route("/health", methods=["GET"])
def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for TrueFoundry monitoring."""
    try:
        # Check if components are initialized
        components_status = {
            "config": config is not None,
            "job_scraper": job_scraper is not None,
            "resume_analyzer": resume_analyzer is not None,
            "job_matcher": job_matcher is not None,
            "resume_optimizer": resume_optimizer is not None,
            "job_applier": job_applier is not None,
            "user_manager": user_manager is not None
        }
        
        all_healthy = all(components_status.values())
        
        return JSONResponse({
            "status": "OK" if all_healthy else "DEGRADED",
            "name": mcp.name,
            "version": "1.0.0",
            "components": components_status,
            "timestamp": str(asyncio.get_event_loop().time()) if asyncio._get_running_loop() else "no-loop"
        })
        
    except Exception as e:
        return JSONResponse({
            "status": "ERROR",
            "name": mcp.name,
            "error": str(e)
        }, status_code=500)

@mcp.custom_route("/status", methods=["GET"])
def status_check(request: Request) -> JSONResponse:
    """Detailed status endpoint."""
    try:
        if not config:
            return JSONResponse({
                "status": "ERROR",
                "message": "Server not initialized"
            }, status_code=503)
        
        validation = config.validate_config()
        
        return JSONResponse({
            "status": "OK",
            "server": mcp.name,
            "version": "1.0.0",
            "configuration": {
                "valid": validation["valid"],
                "issues": validation["issues"]
            },
            "capabilities": {
                "job_search": True,
                "resume_analysis": True,
                "job_matching": True,
                "resume_optimization": validation["config"]["has_openai_key"] or validation["config"]["has_anthropic_key"],
                "job_application": validation["config"]["has_linkedin_credentials"],
                "user_management": True
            }
        })
        
    except Exception as e:
        return JSONResponse({
            "status": "ERROR",
            "error": str(e)
        }, status_code=500)

# --- Server Startup ---

async def startup():
    """Initialize components on server startup."""
    await initialize_components()

# --- Main Entry Point ---

if __name__ == "__main__":
    # Initialize components
    asyncio.run(startup())
    
    # Configure server settings
    from fastmcp import settings
    settings.host = "0.0.0.0"
    settings.port = 8000
    
    logger.info(f"Starting LinkedIn Job Applier FastMCP Server on http://{settings.host}:{settings.port}/mcp")
    
    # Run the server
    mcp.run(transport="streamable-http", stateless_http=True)