"""Main MCP Server for LinkedIn Job Applier"""

import asyncio
import logging
import os
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_job_applier.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LinkedInJobApplierServer:
    """MCP Server for LinkedIn Job Applications"""
    
    def __init__(self):
        self.config = Config()
        self.job_scraper = LinkedInJobScraper(self.config)
        self.resume_analyzer = ResumeAnalyzer(self.config)
        self.job_matcher = JobMatcher(self.config)
        self.resume_optimizer = ResumeOptimizer(self.config)
        self.job_applier = JobApplier(self.config)
        self.user_manager = UserManager(self.config)
        
    async def initialize(self) -> None:
        """Initialize the server components"""
        logger.info("Initializing LinkedIn Job Applier MCP Server")
        await self.user_manager.load_user_data()
        await self.resume_analyzer.initialize()
        logger.info("Server initialization complete")
    
    def get_tools(self) -> List[Tool]:
        """Return list of available MCP tools"""
        return [
            Tool(
                name="search_linkedin_jobs",
                description="Search for LinkedIn job postings from the past month",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "string",
                            "description": "Job search keywords (e.g., 'software engineer python')"
                        },
                        "location": {
                            "type": "string",
                            "description": "Job location (e.g., 'San Francisco, CA' or 'Remote')"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of jobs to return (default: 50)",
                            "default": 50
                        }
                    },
                    "required": ["keywords"]
                }
            ),
            Tool(
                name="analyze_resume",
                description="Analyze resume and extract keywords/skills",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "resume_path": {
                            "type": "string",
                            "description": "Path to resume file (PDF or DOCX)"
                        }
                    },
                    "required": ["resume_path"]
                }
            ),
            Tool(
                name="match_job_resume",
                description="Match job description with resume and calculate compatibility score",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "job_id": {
                            "type": "string",
                            "description": "Job ID from search results"
                        },
                        "job_description": {
                            "type": "string",
                            "description": "Job description text"
                        }
                    },
                    "required": ["job_id", "job_description"]
                }
            ),
            Tool(
                name="optimize_resume",
                description="Generate optimized resume version for specific job",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "job_id": {
                            "type": "string",
                            "description": "Job ID to optimize resume for"
                        },
                        "job_description": {
                            "type": "string",
                            "description": "Job description text"
                        },
                        "optimization_level": {
                            "type": "string",
                            "enum": ["light", "moderate", "aggressive"],
                            "description": "Level of resume optimization",
                            "default": "moderate"
                        }
                    },
                    "required": ["job_id", "job_description"]
                }
            ),
            Tool(
                name="apply_to_job",
                description="Apply to a job with optimized resume",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "job_id": {
                            "type": "string",
                            "description": "Job ID to apply to"
                        },
                        "use_optimized_resume": {
                            "type": "boolean",
                            "description": "Whether to use AI-optimized resume",
                            "default": True
                        },
                        "cover_letter": {
                            "type": "string",
                            "description": "Optional custom cover letter"
                        }
                    },
                    "required": ["job_id"]
                }
            ),
            Tool(
                name="get_application_status",
                description="Get status of job applications",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "days_back": {
                            "type": "integer",
                            "description": "Number of days to look back (default: 7)",
                            "default": 7
                        }
                    }
                }
            ),
            Tool(
                name="update_user_info",
                description="Update user information for job applications",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "field": {
                            "type": "string",
                            "enum": ["personal_info", "preferences", "skills", "experience"],
                            "description": "Type of information to update"
                        },
                        "data": {
                            "type": "object",
                            "description": "Data to update"
                        }
                    },
                    "required": ["field", "data"]
                }
            ),
            Tool(
                name="get_user_info",
                description="Get stored user information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "field": {
                            "type": "string",
                            "enum": ["personal_info", "preferences", "skills", "experience", "all"],
                            "description": "Type of information to retrieve",
                            "default": "all"
                        }
                    }
                }
            )
        ]
    
    async def handle_tool_call(self, request: CallToolRequest) -> CallToolResult:
        """Handle MCP tool calls"""
        try:
            tool_name = request.params.name
            arguments = request.params.arguments or {}
            
            logger.info(f"Handling tool call: {tool_name}")
            
            if tool_name == "search_linkedin_jobs":
                result = await self.job_scraper.search_jobs(
                    keywords=arguments["keywords"],
                    location=arguments.get("location"),
                    max_results=arguments.get("max_results", 50)
                )
                
            elif tool_name == "analyze_resume":
                result = await self.resume_analyzer.analyze_resume(
                    arguments["resume_path"]
                )
                
            elif tool_name == "match_job_resume":
                result = await self.job_matcher.match_job_resume(
                    job_id=arguments["job_id"],
                    job_description=arguments["job_description"]
                )
                
            elif tool_name == "optimize_resume":
                result = await self.resume_optimizer.optimize_resume(
                    job_id=arguments["job_id"],
                    job_description=arguments["job_description"],
                    optimization_level=arguments.get("optimization_level", "moderate")
                )
                
            elif tool_name == "apply_to_job":
                result = await self.job_applier.apply_to_job(
                    job_id=arguments["job_id"],
                    use_optimized_resume=arguments.get("use_optimized_resume", True),
                    cover_letter=arguments.get("cover_letter")
                )
                
            elif tool_name == "get_application_status":
                result = await self.job_applier.get_application_status(
                    days_back=arguments.get("days_back", 7)
                )
                
            elif tool_name == "update_user_info":
                result = await self.user_manager.update_user_info(
                    field=arguments["field"],
                    data=arguments["data"]
                )
                
            elif tool_name == "get_user_info":
                result = await self.user_manager.get_user_info(
                    field=arguments.get("field", "all")
                )
                
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            return CallToolResult(
                content=[TextContent(type="text", text=str(result))]
            )
            
        except Exception as e:
            logger.error(f"Error handling tool call {request.params.name}: {str(e)}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

async def main():
    """Main entry point for the MCP server"""
    server = Server("linkedin-job-applier")
    applier_server = LinkedInJobApplierServer()
    
    @server.list_tools()
    async def handle_list_tools() -> ListToolsResult:
        """Handle list tools request"""
        return ListToolsResult(tools=applier_server.get_tools())
    
    @server.call_tool()
    async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
        """Handle tool call request"""
        return await applier_server.handle_tool_call(request)
    
    # Initialize the server
    await applier_server.initialize()
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="linkedin-job-applier",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())