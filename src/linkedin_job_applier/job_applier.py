"""Automated job application functionality"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc

from .config import Config
from .job_scraper import LinkedInJobScraper
from .user_manager import UserManager

logger = logging.getLogger(__name__)

class JobApplier:
    """Automated job application system"""
    
    def __init__(self, config: Config):
        self.config = config
        self.job_scraper = LinkedInJobScraper(config)
        self.user_manager = UserManager(config)
        self.driver: Optional[webdriver.Chrome] = None
        self.applications_today = 0
        self.max_applications_per_day = config.max_applications_per_day
    
    async def apply_to_job(self, job_id: str, use_optimized_resume: bool = True,
                          cover_letter: Optional[str] = None) -> Dict[str, Any]:
        """Apply to a specific job"""
        try:
            # Check daily application limit
            if not await self._check_application_limit():
                return {"error": "Daily application limit reached"}
            
            # Get job information
            job_info = await self._get_job_info(job_id)
            if not job_info:
                return {"error": f"Job {job_id} not found in cache"}
            
            # Get user information
            user_info = await self.user_manager.get_user_info("all")
            if not user_info or "error" in user_info:
                return {"error": "User information not available. Please update user info first."}
            
            # Determine resume to use
            resume_path = await self._get_resume_path(job_id, use_optimized_resume)
            if not resume_path or not Path(resume_path).exists():
                return {"error": "Resume file not found"}
            
            # Initialize browser if needed
            if not self.driver:
                await self._initialize_browser()
            
            # Navigate to job application page
            application_url = job_info["url"]
            self.driver.get(application_url)
            await asyncio.sleep(2)
            
            # Start application process
            application_result = await self._process_job_application(
                job_info,
                user_info,
                resume_path,
                cover_letter
            )
            
            # Record application
            await self._record_application(job_id, application_result)
            
            if application_result["success"]:
                self.applications_today += 1
            
            return application_result
            
        except Exception as e:
            logger.error(f"Error applying to job {job_id}: {e}")
            return {"error": str(e)}
    
    async def _check_application_limit(self) -> bool:
        """Check if daily application limit has been reached"""
        try:
            # Get today's applications
            today_applications = await self.get_application_status(days_back=1)
            today_count = len([app for app in today_applications 
                             if app.get("applied_at", "").startswith(datetime.now().strftime("%Y-%m-%d"))])
            
            self.applications_today = today_count
            return today_count < self.max_applications_per_day
            
        except Exception as e:
            logger.error(f"Error checking application limit: {e}")
            return False
    
    async def _get_job_info(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job information from cache"""
        try:
            cache_file = self.config.job_cache_file
            if not cache_file.exists():
                return None
            
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            jobs = cache_data.get("jobs", [])
            for job in jobs:
                if job.get("id") == job_id:
                    return job
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting job info: {e}")
            return None
    
    async def _get_resume_path(self, job_id: str, use_optimized: bool) -> Optional[str]:
        """Get the appropriate resume path"""
        if use_optimized:
            # Look for optimized resume
            optimized_dir = self.config.data_dir / "optimized_resumes"
            if optimized_dir.exists():
                # Find the most recent optimized resume for this job
                pattern = f"resume_optimized_{job_id}_*.docx"
                optimized_files = list(optimized_dir.glob(pattern))
                if optimized_files:
                    # Return the most recent one
                    latest_file = max(optimized_files, key=lambda x: x.stat().st_mtime)
                    return str(latest_file)
        
        # Fall back to original resume
        return str(self.config.resume_file)
    
    async def _initialize_browser(self) -> None:
        """Initialize browser for job applications"""
        if not self.job_scraper.logged_in:
            await self.job_scraper.login_to_linkedin()
        
        self.driver = self.job_scraper.driver
    
    async def _process_job_application(self, job_info: Dict[str, Any],
                                     user_info: Dict[str, Any],
                                     resume_path: str,
                                     cover_letter: Optional[str]) -> Dict[str, Any]:
        """Process the actual job application"""
        try:
            # Look for "Easy Apply" button
            easy_apply_button = None
            try:
                easy_apply_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Easy Apply')]"))
                )
            except TimeoutException:
                # Try alternative selectors
                try:
                    easy_apply_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Easy Apply')]")
                except NoSuchElementException:
                    return {
                        "success": False,
                        "error": "Easy Apply button not found",
                        "application_type": "manual_required"
                    }
            
            if not easy_apply_button:
                return {
                    "success": False,
                    "error": "Easy Apply not available for this job",
                    "application_type": "manual_required"
                }
            
            # Click Easy Apply
            easy_apply_button.click()
            await asyncio.sleep(2)
            
            # Process application steps
            steps_completed = []
            current_step = 1
            max_steps = 5  # Prevent infinite loops
            
            while current_step <= max_steps:
                step_result = await self._process_application_step(
                    current_step, user_info, resume_path, cover_letter
                )
                
                steps_completed.append(step_result)
                
                if step_result["completed"]:
                    break
                elif step_result["error"]:
                    return {
                        "success": False,
                        "error": step_result["error"],
                        "steps_completed": steps_completed
                    }
                
                current_step += 1
                await asyncio.sleep(1)
            
            return {
                "success": True,
                "application_type": "easy_apply",
                "steps_completed": steps_completed,
                "applied_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing job application: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _process_application_step(self, step_number: int, user_info: Dict[str, Any],
                                      resume_path: str, cover_letter: Optional[str]) -> Dict[str, Any]:
        """Process a single step of the application"""
        try:
            # Wait for the form to load
            await asyncio.sleep(1)
            
            # Check if this is the final step (submit button)
            submit_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Send')]")
            if submit_buttons:
                # This is the final step
                submit_buttons[0].click()
                await asyncio.sleep(2)
                return {
                    "step": step_number,
                    "type": "submit",
                    "completed": True,
                    "error": None
                }
            
            # Look for "Next" button to continue
            next_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'Continue')]")
            
            # Fill out form fields in this step
            await self._fill_application_form(user_info, resume_path, cover_letter)
            
            # Click next if available
            if next_buttons:
                next_buttons[0].click()
                await asyncio.sleep(2)
                return {
                    "step": step_number,
                    "type": "form_step",
                    "completed": False,
                    "error": None
                }
            else:
                # No next button found, might be completed or error
                return {
                    "step": step_number,
                    "type": "unknown",
                    "completed": True,
                    "error": None
                }
                
        except Exception as e:
            logger.error(f"Error in application step {step_number}: {e}")
            return {
                "step": step_number,
                "type": "error",
                "completed": False,
                "error": str(e)
            }
    
    async def _fill_application_form(self, user_info: Dict[str, Any],
                                   resume_path: str, cover_letter: Optional[str]) -> None:
        """Fill out application form fields"""
        try:
            personal_info = user_info.get("personal_info", {})
            
            # Common form fields and their likely names/IDs
            field_mappings = {
                "firstName": personal_info.get("first_name", ""),
                "lastName": personal_info.get("last_name", ""),
                "email": personal_info.get("email", ""),
                "phone": personal_info.get("phone", ""),
                "location": personal_info.get("location", ""),
                "city": personal_info.get("city", ""),
                "state": personal_info.get("state", ""),
                "country": personal_info.get("country", ""),
                "zipCode": personal_info.get("zip_code", ""),
                "postalCode": personal_info.get("zip_code", ""),
            }
            
            # Fill text fields
            for field_name, value in field_mappings.items():
                if value:
                    await self._fill_field_by_name(field_name, value)
            
            # Handle file upload (resume)
            await self._upload_resume(resume_path)
            
            # Handle cover letter
            if cover_letter:
                await self._fill_cover_letter(cover_letter)
            
            # Handle common questions
            await self._handle_common_questions(user_info)
            
        except Exception as e:
            logger.error(f"Error filling application form: {e}")
    
    async def _fill_field_by_name(self, field_name: str, value: str) -> None:
        """Fill a form field by various possible selectors"""
        selectors = [
            f"input[name='{field_name}']",
            f"input[id='{field_name}']",
            f"input[name*='{field_name}']",
            f"input[id*='{field_name}']",
            f"textarea[name='{field_name}']",
            f"textarea[id='{field_name}']"
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    element = elements[0]
                    element.clear()
                    element.send_keys(value)
                    break
            except Exception:
                continue
    
    async def _upload_resume(self, resume_path: str) -> None:
        """Upload resume file"""
        try:
            # Look for file input elements
            file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            
            for file_input in file_inputs:
                # Check if this is likely a resume upload field
                parent_text = file_input.find_element(By.XPATH, "..").text.lower()
                if any(keyword in parent_text for keyword in ["resume", "cv", "upload"]):
                    file_input.send_keys(resume_path)
                    await asyncio.sleep(2)  # Wait for upload
                    break
                    
        except Exception as e:
            logger.error(f"Error uploading resume: {e}")
    
    async def _fill_cover_letter(self, cover_letter: str) -> None:
        """Fill cover letter field"""
        try:
            # Look for cover letter text areas
            selectors = [
                "textarea[name*='cover']",
                "textarea[id*='cover']",
                "textarea[placeholder*='cover']",
                "textarea[aria-label*='cover']"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        elements[0].clear()
                        elements[0].send_keys(cover_letter)
                        break
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"Error filling cover letter: {e}")
    
    async def _handle_common_questions(self, user_info: Dict[str, Any]) -> None:
        """Handle common application questions"""
        try:
            preferences = user_info.get("preferences", {})
            
            # Common questions and responses
            question_responses = {
                "work authorization": preferences.get("work_authorization", "yes"),
                "visa sponsorship": preferences.get("visa_sponsorship", "no"),
                "willing to relocate": preferences.get("willing_to_relocate", "yes"),
                "remote work": preferences.get("remote_work", "yes"),
                "salary expectation": preferences.get("salary_expectation", ""),
                "start date": preferences.get("start_date", "immediately"),
                "notice period": preferences.get("notice_period", "2 weeks")
            }
            
            # Look for radio buttons, checkboxes, and select elements
            for question_key, response in question_responses.items():
                if response:
                    await self._answer_question(question_key, response)
                    
        except Exception as e:
            logger.error(f"Error handling common questions: {e}")
    
    async def _answer_question(self, question_key: str, response: str) -> None:
        """Answer a specific question"""
        try:
            # Look for elements containing the question text
            question_elements = self.driver.find_elements(
                By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{question_key}')]"
            )
            
            for question_element in question_elements:
                # Find associated input elements
                parent = question_element.find_element(By.XPATH, "..")
                
                # Try radio buttons
                radio_buttons = parent.find_elements(By.CSS_SELECTOR, "input[type='radio']")
                for radio in radio_buttons:
                    label_text = ""
                    try:
                        label = radio.find_element(By.XPATH, "../label")
                        label_text = label.text.lower()
                    except:
                        pass
                    
                    if response.lower() in label_text or (response.lower() == "yes" and "yes" in label_text):
                        radio.click()
                        break
                
                # Try select dropdowns
                selects = parent.find_elements(By.CSS_SELECTOR, "select")
                for select in selects:
                    try:
                        select_element = Select(select)
                        # Try to find option by text
                        for option in select_element.options:
                            if response.lower() in option.text.lower():
                                select_element.select_by_visible_text(option.text)
                                break
                    except Exception:
                        pass
                
                # Try text inputs
                text_inputs = parent.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='number'], textarea")
                for text_input in text_inputs:
                    text_input.clear()
                    text_input.send_keys(response)
                    break
                    
        except Exception as e:
            logger.error(f"Error answering question '{question_key}': {e}")
    
    async def _record_application(self, job_id: str, application_result: Dict[str, Any]) -> None:
        """Record job application in database"""
        try:
            applications_file = self.config.applications_file
            
            # Load existing applications
            applications = []
            if applications_file.exists():
                with open(applications_file, 'r') as f:
                    applications = json.load(f)
            
            # Add new application
            application_record = {
                "job_id": job_id,
                "applied_at": datetime.now().isoformat(),
                "success": application_result.get("success", False),
                "application_type": application_result.get("application_type", "unknown"),
                "error": application_result.get("error"),
                "steps_completed": application_result.get("steps_completed", [])
            }
            
            applications.append(application_record)
            
            # Save updated applications
            with open(applications_file, 'w') as f:
                json.dump(applications, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error recording application: {e}")
    
    async def get_application_status(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Get application status for the specified period"""
        try:
            applications_file = self.config.applications_file
            
            if not applications_file.exists():
                return []
            
            with open(applications_file, 'r') as f:
                applications = json.load(f)
            
            # Filter by date
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            filtered_applications = []
            for app in applications:
                app_date = datetime.fromisoformat(app["applied_at"])
                if app_date >= cutoff_date:
                    filtered_applications.append(app)
            
            # Sort by application date (newest first)
            filtered_applications.sort(key=lambda x: x["applied_at"], reverse=True)
            
            return filtered_applications
            
        except Exception as e:
            logger.error(f"Error getting application status: {e}")
            return []
    
    async def get_application_statistics(self, days_back: int = 30) -> Dict[str, Any]:
        """Get application statistics"""
        try:
            applications = await self.get_application_status(days_back)
            
            total_applications = len(applications)
            successful_applications = len([app for app in applications if app.get("success")])
            failed_applications = total_applications - successful_applications
            
            # Application types
            easy_apply_count = len([app for app in applications if app.get("application_type") == "easy_apply"])
            manual_required_count = len([app for app in applications if app.get("application_type") == "manual_required"])
            
            # Success rate
            success_rate = (successful_applications / total_applications * 100) if total_applications > 0 else 0
            
            return {
                "period_days": days_back,
                "total_applications": total_applications,
                "successful_applications": successful_applications,
                "failed_applications": failed_applications,
                "success_rate": round(success_rate, 1),
                "easy_apply_count": easy_apply_count,
                "manual_required_count": manual_required_count,
                "applications_per_day": round(total_applications / days_back, 1) if days_back > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting application statistics: {e}")
            return {"error": str(e)}
    
    def close(self) -> None:
        """Close the job applier and cleanup resources"""
        if self.job_scraper:
            self.job_scraper.close()
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.close()