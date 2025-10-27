"""LinkedIn job scraping functionality"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode, quote

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

from .config import Config

logger = logging.getLogger(__name__)

class LinkedInJobScraper:
    """Scraper for LinkedIn job postings"""
    
    def __init__(self, config: Config):
        self.config = config
        self.driver: Optional[webdriver.Chrome] = None
        self.session = requests.Session()
        self.user_agent = UserAgent()
        self.logged_in = False
        
        # Set up session headers
        self.session.headers.update({
            'User-Agent': self.user_agent.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def _setup_driver(self) -> webdriver.Chrome:
        """Set up Chrome driver with appropriate options"""
        options = Options()
        
        if self.config.headless_browser:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f'--user-agent={self.user_agent.random}')
        
        # Set download directory
        prefs = {
            "download.default_directory": str(self.config.data_dir / "downloads"),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        
        try:
            driver = uc.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            logger.error(f"Failed to setup Chrome driver: {e}")
            raise
    
    async def login_to_linkedin(self) -> bool:
        """Login to LinkedIn"""
        if not self.config.linkedin_email or not self.config.linkedin_password:
            logger.error("LinkedIn credentials not configured")
            return False
        
        try:
            if not self.driver:
                self.driver = self._setup_driver()
            
            logger.info("Logging into LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for login form
            wait = WebDriverWait(self.driver, self.config.browser_timeout)
            
            # Enter email
            email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
            email_field.clear()
            email_field.send_keys(self.config.linkedin_email)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(self.config.linkedin_password)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete
            await asyncio.sleep(3)
            
            # Check if we're logged in by looking for the feed or profile
            try:
                wait.until(EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "global-nav")),
                    EC.presence_of_element_located((By.CLASS_NAME, "feed-container"))
                ))
                self.logged_in = True
                logger.info("Successfully logged into LinkedIn")
                return True
            except TimeoutException:
                logger.error("Login failed - could not find expected elements")
                return False
                
        except Exception as e:
            logger.error(f"Error during LinkedIn login: {e}")
            return False
    
    async def search_jobs(self, keywords: str, location: Optional[str] = None, 
                         max_results: int = 50) -> Dict[str, Any]:
        """Search for LinkedIn jobs"""
        try:
            if not self.logged_in:
                if not await self.login_to_linkedin():
                    return {"error": "Failed to login to LinkedIn"}
            
            logger.info(f"Searching for jobs: {keywords}")
            
            # Build search URL
            search_params = {
                'keywords': keywords,
                'f_TPR': 'r2592000',  # Past month
                'f_JT': 'F',  # Full-time
                'sortBy': 'DD',  # Date posted
            }
            
            if location:
                search_params['location'] = location
            
            search_url = f"https://www.linkedin.com/jobs/search/?{urlencode(search_params)}"
            
            self.driver.get(search_url)
            await asyncio.sleep(2)
            
            jobs = []
            page = 1
            
            while len(jobs) < max_results and page <= 10:  # Limit to 10 pages
                logger.info(f"Scraping page {page}")
                
                # Wait for job listings to load
                wait = WebDriverWait(self.driver, self.config.browser_timeout)
                try:
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list")))
                except TimeoutException:
                    logger.warning("No job listings found on this page")
                    break
                
                # Extract job listings
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job-search-card")
                
                for card in job_cards:
                    if len(jobs) >= max_results:
                        break
                    
                    try:
                        job_data = await self._extract_job_data(card)
                        if job_data:
                            jobs.append(job_data)
                    except Exception as e:
                        logger.warning(f"Error extracting job data: {e}")
                        continue
                
                # Try to go to next page
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next']")
                    if next_button.is_enabled():
                        next_button.click()
                        await asyncio.sleep(2)
                        page += 1
                    else:
                        break
                except NoSuchElementException:
                    break
            
            # Cache results
            await self._cache_jobs(jobs)
            
            return {
                "success": True,
                "jobs_found": len(jobs),
                "jobs": jobs,
                "search_params": {
                    "keywords": keywords,
                    "location": location,
                    "max_results": max_results
                }
            }
            
        except Exception as e:
            logger.error(f"Error searching jobs: {e}")
            return {"error": str(e)}
    
    async def _extract_job_data(self, job_card) -> Optional[Dict[str, Any]]:
        """Extract job data from a job card element"""
        try:
            # Basic job information
            title_element = job_card.find_element(By.CSS_SELECTOR, ".job-search-card__title a")
            title = title_element.text.strip()
            job_url = title_element.get_attribute("href")
            job_id = job_url.split("/")[-2] if job_url else None
            
            company_element = job_card.find_element(By.CSS_SELECTOR, ".job-search-card__subtitle a")
            company = company_element.text.strip()
            
            location_element = job_card.find_element(By.CSS_SELECTOR, ".job-search-card__location")
            location = location_element.text.strip()
            
            # Posted date
            posted_element = job_card.find_element(By.CSS_SELECTOR, ".job-search-card__listdate")
            posted_date = posted_element.get_attribute("datetime")
            
            # Get job description by clicking on the job
            description = await self._get_job_description(job_url)
            
            job_data = {
                "id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "url": job_url,
                "posted_date": posted_date,
                "description": description,
                "scraped_at": datetime.now().isoformat(),
                "applied": False,
                "match_score": None,
            }
            
            return job_data
            
        except Exception as e:
            logger.warning(f"Error extracting job data: {e}")
            return None
    
    async def _get_job_description(self, job_url: str) -> str:
        """Get full job description from job URL"""
        try:
            # Open job in new tab
            self.driver.execute_script(f"window.open('{job_url}', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            # Wait for job description to load
            wait = WebDriverWait(self.driver, 10)
            description_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-description-content__text"))
            )
            
            description = description_element.text.strip()
            
            # Close tab and switch back
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            return description
            
        except Exception as e:
            logger.warning(f"Error getting job description: {e}")
            return ""
    
    async def _cache_jobs(self, jobs: List[Dict[str, Any]]) -> None:
        """Cache job data to file"""
        try:
            cache_data = {
                "last_updated": datetime.now().isoformat(),
                "jobs": jobs
            }
            
            with open(self.config.job_cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error caching jobs: {e}")
    
    async def get_cached_jobs(self, max_age_hours: int = 24) -> List[Dict[str, Any]]:
        """Get cached job data if not too old"""
        try:
            if not self.config.job_cache_file.exists():
                return []
            
            with open(self.config.job_cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache is still valid
            last_updated = datetime.fromisoformat(cache_data["last_updated"])
            if datetime.now() - last_updated > timedelta(hours=max_age_hours):
                return []
            
            return cache_data.get("jobs", [])
            
        except Exception as e:
            logger.error(f"Error reading cached jobs: {e}")
            return []
    
    def close(self) -> None:
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.logged_in = False
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.close()