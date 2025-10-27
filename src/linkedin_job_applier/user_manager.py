"""User information management and storage"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import asyncio

from .config import Config

logger = logging.getLogger(__name__)

class UserManager:
    """Manage user information and preferences"""
    
    def __init__(self, config: Config):
        self.config = config
        self.user_data: Dict[str, Any] = {}
        self.user_data_file = config.user_data_file
        
        # Default user data structure
        self.default_user_data = {
            "personal_info": {
                "first_name": "",
                "last_name": "",
                "email": "",
                "phone": "",
                "location": "",
                "city": "",
                "state": "",
                "country": "",
                "zip_code": "",
                "linkedin_profile": "",
                "github_profile": "",
                "website": ""
            },
            "preferences": {
                "work_authorization": "",  # yes/no
                "visa_sponsorship": "",    # yes/no
                "willing_to_relocate": "", # yes/no
                "remote_work": "",         # yes/no/preferred
                "salary_expectation": "",
                "start_date": "",          # immediately/2weeks/1month/etc
                "notice_period": "",       # 2weeks/1month/etc
                "preferred_locations": [],
                "job_types": [],           # full-time/part-time/contract
                "industries": [],
                "company_sizes": []        # startup/small/medium/large/enterprise
            },
            "skills": {
                "technical_skills": [],
                "soft_skills": [],
                "certifications": [],
                "languages": []
            },
            "experience": {
                "years_total": 0,
                "current_title": "",
                "current_company": "",
                "previous_roles": [],
                "education": [],
                "projects": []
            },
            "application_settings": {
                "auto_apply_threshold": 0.7,  # Minimum match score for auto-apply
                "max_applications_per_day": 10,
                "preferred_resume_optimization": "moderate",  # light/moderate/aggressive
                "cover_letter_template": "",
                "follow_up_enabled": False,
                "application_tracking": True
            },
            "metadata": {
                "created_at": "",
                "last_updated": "",
                "version": "1.0"
            }
        }
    
    async def load_user_data(self) -> None:
        """Load user data from file"""
        try:
            if self.user_data_file.exists():
                with open(self.user_data_file, 'r') as f:
                    self.user_data = json.load(f)
                logger.info("User data loaded successfully")
            else:
                # Initialize with default data
                self.user_data = self.default_user_data.copy()
                self.user_data["metadata"]["created_at"] = datetime.now().isoformat()
                await self.save_user_data()
                logger.info("Initialized new user data file")
                
        except Exception as e:
            logger.error(f"Error loading user data: {e}")
            self.user_data = self.default_user_data.copy()
    
    async def save_user_data(self) -> None:
        """Save user data to file"""
        try:
            self.user_data["metadata"]["last_updated"] = datetime.now().isoformat()
            
            with open(self.user_data_file, 'w') as f:
                json.dump(self.user_data, f, indent=2)
                
            logger.info("User data saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving user data: {e}")
            raise
    
    async def update_user_info(self, field: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user information"""
        try:
            if field not in ["personal_info", "preferences", "skills", "experience", "application_settings"]:
                return {"error": f"Invalid field: {field}"}
            
            if field not in self.user_data:
                self.user_data[field] = {}
            
            # Update the specified field
            self.user_data[field].update(data)
            
            # Save changes
            await self.save_user_data()
            
            return {
                "success": True,
                "field": field,
                "updated_data": self.user_data[field]
            }
            
        except Exception as e:
            logger.error(f"Error updating user info: {e}")
            return {"error": str(e)}
    
    async def get_user_info(self, field: str = "all") -> Dict[str, Any]:
        """Get user information"""
        try:
            if field == "all":
                return {
                    "success": True,
                    "user_data": self.user_data
                }
            elif field in self.user_data:
                return {
                    "success": True,
                    "field": field,
                    "data": self.user_data[field]
                }
            else:
                return {"error": f"Field '{field}' not found"}
                
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return {"error": str(e)}
    
    async def check_required_info(self, application_type: str = "basic") -> Dict[str, Any]:
        """Check if required information is available for job applications"""
        try:
            missing_info = []
            warnings = []
            
            personal_info = self.user_data.get("personal_info", {})
            preferences = self.user_data.get("preferences", {})
            
            # Required personal information
            required_personal = ["first_name", "last_name", "email", "phone"]
            for field in required_personal:
                if not personal_info.get(field):
                    missing_info.append(f"personal_info.{field}")
            
            # Important preferences for applications
            important_preferences = ["work_authorization", "visa_sponsorship"]
            for field in important_preferences:
                if not preferences.get(field):
                    warnings.append(f"preferences.{field}")
            
            # Check if resume is available
            if not self.config.resume_file.exists():
                missing_info.append("resume_file")
            
            return {
                "ready_for_applications": len(missing_info) == 0,
                "missing_required": missing_info,
                "missing_recommended": warnings,
                "completeness_score": self._calculate_completeness_score()
            }
            
        except Exception as e:
            logger.error(f"Error checking required info: {e}")
            return {"error": str(e)}
    
    def _calculate_completeness_score(self) -> float:
        """Calculate user data completeness score (0-1)"""
        try:
            total_fields = 0
            completed_fields = 0
            
            # Count personal info fields
            personal_info = self.user_data.get("personal_info", {})
            for key, value in personal_info.items():
                total_fields += 1
                if value:
                    completed_fields += 1
            
            # Count preferences fields
            preferences = self.user_data.get("preferences", {})
            for key, value in preferences.items():
                total_fields += 1
                if value:
                    completed_fields += 1
            
            # Count skills
            skills = self.user_data.get("skills", {})
            for key, value in skills.items():
                total_fields += 1
                if value:
                    completed_fields += 1
            
            # Count experience
            experience = self.user_data.get("experience", {})
            for key, value in experience.items():
                total_fields += 1
                if value:
                    completed_fields += 1
            
            return completed_fields / total_fields if total_fields > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating completeness score: {e}")
            return 0.0
    
    async def prompt_for_missing_info(self, missing_fields: List[str]) -> Dict[str, Any]:
        """Generate prompts for missing information"""
        try:
            prompts = []
            
            field_descriptions = {
                "personal_info.first_name": {
                    "prompt": "What is your first name?",
                    "type": "text",
                    "required": True
                },
                "personal_info.last_name": {
                    "prompt": "What is your last name?",
                    "type": "text",
                    "required": True
                },
                "personal_info.email": {
                    "prompt": "What is your email address?",
                    "type": "email",
                    "required": True
                },
                "personal_info.phone": {
                    "prompt": "What is your phone number?",
                    "type": "tel",
                    "required": True
                },
                "personal_info.location": {
                    "prompt": "What is your current location (City, State)?",
                    "type": "text",
                    "required": False
                },
                "preferences.work_authorization": {
                    "prompt": "Are you authorized to work in this country?",
                    "type": "select",
                    "options": ["yes", "no"],
                    "required": True
                },
                "preferences.visa_sponsorship": {
                    "prompt": "Do you require visa sponsorship?",
                    "type": "select",
                    "options": ["yes", "no"],
                    "required": True
                },
                "preferences.willing_to_relocate": {
                    "prompt": "Are you willing to relocate for work?",
                    "type": "select",
                    "options": ["yes", "no", "depends"],
                    "required": False
                },
                "preferences.remote_work": {
                    "prompt": "What is your preference for remote work?",
                    "type": "select",
                    "options": ["yes", "no", "hybrid", "preferred"],
                    "required": False
                },
                "preferences.salary_expectation": {
                    "prompt": "What is your salary expectation (optional)?",
                    "type": "text",
                    "required": False
                },
                "preferences.start_date": {
                    "prompt": "When can you start?",
                    "type": "select",
                    "options": ["immediately", "2 weeks", "1 month", "2 months", "3+ months"],
                    "required": False
                }
            }
            
            for field in missing_fields:
                if field in field_descriptions:
                    prompt_info = field_descriptions[field].copy()
                    prompt_info["field"] = field
                    prompts.append(prompt_info)
            
            return {
                "success": True,
                "prompts": prompts,
                "total_prompts": len(prompts)
            }
            
        except Exception as e:
            logger.error(f"Error generating prompts: {e}")
            return {"error": str(e)}
    
    async def process_user_responses(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Process user responses to information prompts"""
        try:
            updated_fields = []
            
            for field_path, value in responses.items():
                if not value:  # Skip empty values
                    continue
                
                # Parse field path (e.g., "personal_info.first_name")
                parts = field_path.split(".")
                if len(parts) != 2:
                    continue
                
                section, field = parts
                
                # Update the data
                if section not in self.user_data:
                    self.user_data[section] = {}
                
                self.user_data[section][field] = value
                updated_fields.append(field_path)
            
            # Save changes
            if updated_fields:
                await self.save_user_data()
            
            return {
                "success": True,
                "updated_fields": updated_fields,
                "completeness_score": self._calculate_completeness_score()
            }
            
        except Exception as e:
            logger.error(f"Error processing user responses: {e}")
            return {"error": str(e)}
    
    async def get_application_preferences(self) -> Dict[str, Any]:
        """Get user preferences for job applications"""
        try:
            preferences = self.user_data.get("preferences", {})
            app_settings = self.user_data.get("application_settings", {})
            
            return {
                "auto_apply_threshold": app_settings.get("auto_apply_threshold", 0.7),
                "max_applications_per_day": app_settings.get("max_applications_per_day", 10),
                "preferred_resume_optimization": app_settings.get("preferred_resume_optimization", "moderate"),
                "work_authorization": preferences.get("work_authorization", ""),
                "visa_sponsorship": preferences.get("visa_sponsorship", ""),
                "willing_to_relocate": preferences.get("willing_to_relocate", ""),
                "remote_work": preferences.get("remote_work", ""),
                "salary_expectation": preferences.get("salary_expectation", ""),
                "start_date": preferences.get("start_date", ""),
                "notice_period": preferences.get("notice_period", ""),
                "preferred_locations": preferences.get("preferred_locations", []),
                "job_types": preferences.get("job_types", [])
            }
            
        except Exception as e:
            logger.error(f"Error getting application preferences: {e}")
            return {"error": str(e)}
    
    async def update_application_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update application-specific settings"""
        try:
            if "application_settings" not in self.user_data:
                self.user_data["application_settings"] = {}
            
            # Update settings
            self.user_data["application_settings"].update(settings)
            
            # Save changes
            await self.save_user_data()
            
            return {
                "success": True,
                "updated_settings": self.user_data["application_settings"]
            }
            
        except Exception as e:
            logger.error(f"Error updating application settings: {e}")
            return {"error": str(e)}
    
    async def export_user_data(self, export_path: Optional[str] = None) -> Dict[str, Any]:
        """Export user data to a file"""
        try:
            if not export_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                export_path = str(self.config.data_dir / f"user_data_export_{timestamp}.json")
            
            export_data = {
                "exported_at": datetime.now().isoformat(),
                "user_data": self.user_data,
                "config_summary": {
                    "max_applications_per_day": self.config.max_applications_per_day,
                    "minimum_match_score": self.config.minimum_match_score,
                    "resume_file": str(self.config.resume_file)
                }
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return {
                "success": True,
                "export_path": export_path,
                "exported_at": export_data["exported_at"]
            }
            
        except Exception as e:
            logger.error(f"Error exporting user data: {e}")
            return {"error": str(e)}
    
    async def import_user_data(self, import_path: str, merge: bool = True) -> Dict[str, Any]:
        """Import user data from a file"""
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                return {"error": f"Import file not found: {import_path}"}
            
            with open(import_file, 'r') as f:
                import_data = json.load(f)
            
            if "user_data" not in import_data:
                return {"error": "Invalid import file format"}
            
            if merge:
                # Merge with existing data
                for section, data in import_data["user_data"].items():
                    if section in self.user_data:
                        if isinstance(data, dict):
                            self.user_data[section].update(data)
                        else:
                            self.user_data[section] = data
                    else:
                        self.user_data[section] = data
            else:
                # Replace existing data
                self.user_data = import_data["user_data"]
            
            # Save changes
            await self.save_user_data()
            
            return {
                "success": True,
                "imported_from": import_path,
                "merge_mode": merge,
                "completeness_score": self._calculate_completeness_score()
            }
            
        except Exception as e:
            logger.error(f"Error importing user data: {e}")
            return {"error": str(e)}
    
    async def get_user_summary(self) -> Dict[str, Any]:
        """Get a summary of user information"""
        try:
            personal_info = self.user_data.get("personal_info", {})
            preferences = self.user_data.get("preferences", {})
            skills = self.user_data.get("skills", {})
            experience = self.user_data.get("experience", {})
            
            return {
                "name": f"{personal_info.get('first_name', '')} {personal_info.get('last_name', '')}".strip(),
                "email": personal_info.get("email", ""),
                "location": personal_info.get("location", ""),
                "experience_years": experience.get("years_total", 0),
                "current_role": experience.get("current_title", ""),
                "technical_skills_count": len(skills.get("technical_skills", [])),
                "work_authorization": preferences.get("work_authorization", ""),
                "remote_preference": preferences.get("remote_work", ""),
                "completeness_score": round(self._calculate_completeness_score() * 100, 1),
                "last_updated": self.user_data.get("metadata", {}).get("last_updated", ""),
                "ready_for_applications": len(await self.check_required_info()) == 0
            }
            
        except Exception as e:
            logger.error(f"Error getting user summary: {e}")
            return {"error": str(e)}