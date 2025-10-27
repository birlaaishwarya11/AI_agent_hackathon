#!/usr/bin/env python3
"""Demo script for LinkedIn Job Applier MCP Server"""

import asyncio
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from linkedin_job_applier.config import Config
from linkedin_job_applier.resume_analyzer import ResumeAnalyzer
from linkedin_job_applier.job_matcher import JobMatcher
from linkedin_job_applier.user_manager import UserManager

async def demo_resume_analysis():
    """Demo resume analysis functionality"""
    print("\n" + "="*60)
    print("DEMO: Resume Analysis")
    print("="*60)
    
    config = Config()
    analyzer = ResumeAnalyzer(config)
    
    # Initialize analyzer
    await analyzer.initialize()
    
    # Analyze sample resume
    resume_path = str(config.data_dir / "sample_resume.txt")
    print(f"Analyzing resume: {resume_path}")
    
    result = await analyzer.analyze_resume(resume_path)
    
    if result.get("success"):
        analysis = result["analysis"]
        print(f"\n✅ Resume Analysis Results:")
        print(f"   Word count: {analysis['word_count']}")
        print(f"   Technical skills found: {len(analysis['technical_skills'])}")
        print(f"   Technical skills: {', '.join(analysis['technical_skills'][:10])}")
        print(f"   Soft skills: {', '.join(analysis['soft_skills'][:5])}")
        print(f"   Experience years: {analysis.get('experience_years', 'Not detected')}")
        print(f"   Top keywords: {', '.join(analysis['keywords'][:8])}")
        
        # Get skills summary
        skills_summary = analyzer.get_skills_summary()
        print(f"   Total skills detected: {skills_summary['total_skills']}")
        
    else:
        print(f"❌ Resume analysis failed: {result.get('error')}")
    
    return result

async def demo_job_matching():
    """Demo job matching functionality"""
    print("\n" + "="*60)
    print("DEMO: Job-Resume Matching")
    print("="*60)
    
    config = Config()
    matcher = JobMatcher(config)
    
    # Sample job description
    job_description = """
    Senior Software Engineer - Python/React
    
    We are looking for a Senior Software Engineer with 3-5 years of experience 
    to join our growing team. The ideal candidate will have strong experience 
    with Python, React, and cloud technologies.
    
    Required Skills:
    - 3+ years of Python development experience
    - Experience with React and modern JavaScript
    - Knowledge of PostgreSQL or similar databases
    - Experience with AWS or other cloud platforms
    - Strong understanding of RESTful APIs
    - Experience with Docker and containerization
    
    Preferred Skills:
    - Experience with Kubernetes
    - Knowledge of Django or Flask frameworks
    - Experience with CI/CD pipelines
    - Agile development experience
    
    We offer competitive salary, excellent benefits, and the opportunity 
    to work on cutting-edge technology in a collaborative environment.
    """
    
    print("Matching sample job description with resume...")
    print(f"Job description preview: {job_description[:200]}...")
    
    # Perform matching
    match_result = await matcher.match_job_resume("demo_job_001", job_description)
    
    if match_result.get("success"):
        match_data = match_result["match_result"]
        print(f"\n✅ Job Matching Results:")
        print(f"   Overall match score: {match_data['overall_score']:.1%}")
        print(f"   Technical skills match: {match_data['category_scores']['technical_skills']:.1%}")
        print(f"   Experience match: {match_data['category_scores']['experience']:.1%}")
        print(f"   Keyword similarity: {match_data['category_scores']['keywords']:.1%}")
        print(f"   Must-have requirements: {match_data['category_scores']['must_have']:.1%}")
        
        print(f"\n   Skills matched: {', '.join(match_data['requirements_met']['technical_skills'][:5])}")
        print(f"   Skills missing: {', '.join(match_data['requirements_missing']['technical_skills'][:3])}")
        print(f"   Recommendation: {match_data['recommendation']}")
        
        # Show detailed analysis
        analysis = match_data['detailed_analysis']
        if analysis['strengths']:
            print(f"   Strengths: {', '.join(analysis['strengths'])}")
        if analysis['recommendations']:
            print(f"   Recommendations: {analysis['recommendations'][0]}")
            
    else:
        print(f"❌ Job matching failed: {match_result.get('error')}")
    
    return match_result

async def demo_user_management():
    """Demo user information management"""
    print("\n" + "="*60)
    print("DEMO: User Information Management")
    print("="*60)
    
    config = Config()
    user_manager = UserManager(config)
    
    # Load user data
    await user_manager.load_user_data()
    
    # Update sample user information
    print("Setting up sample user information...")
    
    personal_info = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@email.com",
        "phone": "(555) 123-4567",
        "location": "San Francisco, CA",
        "linkedin_profile": "linkedin.com/in/johndoe"
    }
    
    preferences = {
        "work_authorization": "yes",
        "visa_sponsorship": "no",
        "willing_to_relocate": "yes",
        "remote_work": "preferred",
        "salary_expectation": "$120,000 - $150,000",
        "start_date": "2 weeks",
        "preferred_locations": ["San Francisco", "New York", "Remote"]
    }
    
    # Update user info
    await user_manager.update_user_info("personal_info", personal_info)
    await user_manager.update_user_info("preferences", preferences)
    
    # Check required info
    required_check = await user_manager.check_required_info()
    print(f"\n✅ User Information Status:")
    print(f"   Ready for applications: {required_check['ready_for_applications']}")
    print(f"   Completeness score: {required_check['completeness_score']:.1%}")
    
    if required_check['missing_required']:
        print(f"   Missing required: {', '.join(required_check['missing_required'])}")
    
    if required_check['missing_recommended']:
        print(f"   Missing recommended: {', '.join(required_check['missing_recommended'])}")
    
    # Get user summary
    summary = await user_manager.get_user_summary()
    print(f"\n   User: {summary['name']}")
    print(f"   Email: {summary['email']}")
    print(f"   Location: {summary['location']}")
    print(f"   Work authorization: {summary['work_authorization']}")
    print(f"   Remote preference: {summary['remote_preference']}")
    
    return summary

async def demo_configuration():
    """Demo configuration management"""
    print("\n" + "="*60)
    print("DEMO: Configuration Management")
    print("="*60)
    
    config = Config()
    
    print("Configuration Summary:")
    print(config)
    
    validation = config.validate_config()
    print(f"\nConfiguration Status:")
    print(f"   Valid: {validation['valid']}")
    
    if validation['issues']:
        print(f"   Issues to resolve:")
        for issue in validation['issues']:
            print(f"     - {issue}")
    
    print(f"\nConfiguration Details:")
    config_details = validation['config']
    for key, value in config_details.items():
        print(f"   {key}: {value}")
    
    return validation

async def main():
    """Run all demos"""
    print("🚀 LinkedIn Job Applier MCP Server - Demo")
    print("This demo showcases the key features of the system")
    
    try:
        # Demo configuration
        await demo_configuration()
        
        # Demo resume analysis
        await demo_resume_analysis()
        
        # Demo job matching
        await demo_job_matching()
        
        # Demo user management
        await demo_user_management()
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        print("\nNext Steps:")
        print("1. Set up real LinkedIn credentials in .env file")
        print("2. Add your OpenAI or Anthropic API key")
        print("3. Upload your actual resume (PDF or DOCX)")
        print("4. Run the MCP server: linkedin-job-applier")
        print("5. Connect from your MCP client to start applying to jobs!")
        
        print("\nMCP Tools Available:")
        print("- search_linkedin_jobs: Find relevant job postings")
        print("- analyze_resume: Extract skills and keywords from resume")
        print("- match_job_resume: Calculate job-resume compatibility")
        print("- optimize_resume: AI-powered resume optimization")
        print("- apply_to_job: Automated job application")
        print("- update_user_info: Manage personal information")
        print("- get_application_status: Track application history")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)