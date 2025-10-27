"""Job-resume matching algorithm"""

import logging
import re
from typing import Dict, List, Any, Optional, Tuple
import json
from datetime import datetime, timedelta

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from .config import Config
from .resume_analyzer import ResumeAnalyzer

logger = logging.getLogger(__name__)

class JobMatcher:
    """Match job descriptions with resume content"""
    
    def __init__(self, config: Config):
        self.config = config
        self.resume_analyzer = ResumeAnalyzer(config)
        self.lemmatizer = WordNetLemmatizer()
        
        # Initialize NLTK data
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            # Download required NLTK data if not available
            nltk.download('stopwords', quiet=True)
            self.stop_words = set(stopwords.words('english'))
        
        # Job requirement keywords by category
        self.requirement_categories = {
            'technical_skills': {
                'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'ruby'],
                'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask'],
                'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch'],
                'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
                'data': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'spark'],
                'tools': ['git', 'jenkins', 'jira', 'linux', 'bash', 'vim']
            },
            'soft_skills': {
                'leadership': ['leadership', 'management', 'mentoring', 'coaching', 'team lead'],
                'communication': ['communication', 'presentation', 'writing', 'documentation'],
                'collaboration': ['teamwork', 'collaboration', 'cross-functional', 'agile', 'scrum'],
                'problem_solving': ['problem-solving', 'analytical', 'critical thinking', 'debugging']
            },
            'experience_levels': {
                'entry': ['entry level', 'junior', '0-2 years', 'new grad', 'recent graduate'],
                'mid': ['mid level', 'intermediate', '3-5 years', 'experienced'],
                'senior': ['senior', 'lead', '5+ years', '7+ years', 'expert', 'principal'],
                'executive': ['director', 'vp', 'cto', 'head of', 'chief']
            }
        }
    
    async def match_job_resume(self, job_id: str, job_description: str) -> Dict[str, Any]:
        """Match a job description with the user's resume"""
        try:
            # Get resume data
            resume_data = await self.resume_analyzer.get_resume_data()
            if not resume_data:
                return {"error": "No resume analysis available. Please analyze resume first."}
            
            # Extract job requirements
            job_requirements = await self._extract_job_requirements(job_description)
            
            # Calculate match scores
            match_scores = await self._calculate_match_scores(
                resume_data["analysis"], 
                job_requirements,
                job_description
            )
            
            # Generate detailed analysis
            detailed_analysis = await self._generate_detailed_analysis(
                resume_data["analysis"],
                job_requirements,
                match_scores
            )
            
            # Create match result
            match_result = {
                "job_id": job_id,
                "overall_score": match_scores["overall"],
                "category_scores": match_scores["categories"],
                "requirements_met": match_scores["requirements_met"],
                "requirements_missing": match_scores["requirements_missing"],
                "detailed_analysis": detailed_analysis,
                "recommendation": self._get_recommendation(match_scores["overall"]),
                "matched_at": datetime.now().isoformat()
            }
            
            # Save match result
            await self._save_match_result(job_id, match_result)
            
            return {
                "success": True,
                "match_result": match_result
            }
            
        except Exception as e:
            logger.error(f"Error matching job with resume: {e}")
            return {"error": str(e)}
    
    async def _extract_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """Extract requirements from job description"""
        job_text = job_description.lower()
        
        requirements = {
            "technical_skills": [],
            "soft_skills": [],
            "experience_level": None,
            "education": [],
            "certifications": [],
            "must_have": [],
            "nice_to_have": [],
            "years_experience": None
        }
        
        # Extract technical skills
        for category, skills in self.requirement_categories['technical_skills'].items():
            for skill in skills:
                if skill.lower() in job_text:
                    requirements["technical_skills"].append(skill)
        
        # Extract soft skills
        for category, skills in self.requirement_categories['soft_skills'].items():
            for skill in skills:
                if skill.lower() in job_text:
                    requirements["soft_skills"].append(skill)
        
        # Extract experience level
        for level, indicators in self.requirement_categories['experience_levels'].items():
            for indicator in indicators:
                if indicator.lower() in job_text:
                    requirements["experience_level"] = level
                    break
            if requirements["experience_level"]:
                break
        
        # Extract years of experience
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*of\s*experience',
            r'(\d+)\+?\s*years?\s*experience',
            r'minimum\s*(\d+)\s*years?',
            r'at least\s*(\d+)\s*years?'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, job_text)
            if match:
                requirements["years_experience"] = int(match.group(1))
                break
        
        # Extract education requirements
        education_patterns = [
            r'(bachelor|master|phd|doctorate).*?(degree|in)\s+([^\n\.]+)',
            r'(b\.?s\.?|m\.?s\.?|ph\.?d\.?)\s+([^\n\.]+)',
            r'degree\s+in\s+([^\n\.]+)'
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, job_text)
            requirements["education"].extend([' '.join(match) for match in matches])
        
        # Extract must-have vs nice-to-have
        must_have_section = re.search(r'(required|must have|essential).*?(?=preferred|nice to have|plus|bonus|\n\n)', job_text, re.DOTALL | re.IGNORECASE)
        if must_have_section:
            requirements["must_have"] = self._extract_skills_from_text(must_have_section.group())
        
        nice_to_have_section = re.search(r'(preferred|nice to have|plus|bonus).*?(?=\n\n|$)', job_text, re.DOTALL | re.IGNORECASE)
        if nice_to_have_section:
            requirements["nice_to_have"] = self._extract_skills_from_text(nice_to_have_section.group())
        
        return requirements
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from a text section"""
        skills = []
        
        # Look for technical skills
        for category, skill_list in self.requirement_categories['technical_skills'].items():
            for skill in skill_list:
                if skill.lower() in text.lower():
                    skills.append(skill)
        
        # Look for soft skills
        for category, skill_list in self.requirement_categories['soft_skills'].items():
            for skill in skill_list:
                if skill.lower() in text.lower():
                    skills.append(skill)
        
        return list(set(skills))
    
    async def _calculate_match_scores(self, resume_analysis: Dict[str, Any], 
                                    job_requirements: Dict[str, Any],
                                    job_description: str) -> Dict[str, Any]:
        """Calculate various match scores"""
        
        # Technical skills match
        resume_tech_skills = set(skill.lower() for skill in resume_analysis.get("technical_skills", []))
        job_tech_skills = set(skill.lower() for skill in job_requirements.get("technical_skills", []))
        
        tech_match = len(resume_tech_skills.intersection(job_tech_skills))
        tech_total = len(job_tech_skills) if job_tech_skills else 1
        tech_score = tech_match / tech_total
        
        # Soft skills match
        resume_soft_skills = set(skill.lower() for skill in resume_analysis.get("soft_skills", []))
        job_soft_skills = set(skill.lower() for skill in job_requirements.get("soft_skills", []))
        
        soft_match = len(resume_soft_skills.intersection(job_soft_skills))
        soft_total = len(job_soft_skills) if job_soft_skills else 1
        soft_score = soft_match / soft_total
        
        # Experience level match
        experience_score = self._calculate_experience_match(
            resume_analysis.get("experience_years"),
            job_requirements.get("years_experience"),
            job_requirements.get("experience_level")
        )
        
        # Keyword similarity using TF-IDF
        keyword_score = await self._calculate_keyword_similarity(
            resume_analysis.get("keywords", []),
            job_description
        )
        
        # Must-have requirements
        must_have_skills = set(skill.lower() for skill in job_requirements.get("must_have", []))
        must_have_met = resume_tech_skills.union(resume_soft_skills).intersection(must_have_skills)
        must_have_score = len(must_have_met) / len(must_have_skills) if must_have_skills else 1.0
        
        # Nice-to-have requirements
        nice_to_have_skills = set(skill.lower() for skill in job_requirements.get("nice_to_have", []))
        nice_to_have_met = resume_tech_skills.union(resume_soft_skills).intersection(nice_to_have_skills)
        nice_to_have_score = len(nice_to_have_met) / len(nice_to_have_skills) if nice_to_have_skills else 0.0
        
        # Calculate overall score with weights
        weights = {
            "technical": 0.3,
            "soft_skills": 0.15,
            "experience": 0.25,
            "keywords": 0.15,
            "must_have": 0.15
        }
        
        overall_score = (
            tech_score * weights["technical"] +
            soft_score * weights["soft_skills"] +
            experience_score * weights["experience"] +
            keyword_score * weights["keywords"] +
            must_have_score * weights["must_have"]
        )
        
        return {
            "overall": round(overall_score, 3),
            "categories": {
                "technical_skills": round(tech_score, 3),
                "soft_skills": round(soft_score, 3),
                "experience": round(experience_score, 3),
                "keywords": round(keyword_score, 3),
                "must_have": round(must_have_score, 3),
                "nice_to_have": round(nice_to_have_score, 3)
            },
            "requirements_met": {
                "technical_skills": list(resume_tech_skills.intersection(job_tech_skills)),
                "soft_skills": list(resume_soft_skills.intersection(job_soft_skills)),
                "must_have": list(must_have_met),
                "nice_to_have": list(nice_to_have_met)
            },
            "requirements_missing": {
                "technical_skills": list(job_tech_skills - resume_tech_skills),
                "soft_skills": list(job_soft_skills - resume_soft_skills),
                "must_have": list(must_have_skills - must_have_met),
                "nice_to_have": list(nice_to_have_skills - nice_to_have_met)
            }
        }
    
    def _calculate_experience_match(self, resume_years: Optional[int], 
                                  job_years: Optional[int],
                                  job_level: Optional[str]) -> float:
        """Calculate experience level match score"""
        if not resume_years:
            return 0.5  # Neutral score if no experience data
        
        if job_years:
            if resume_years >= job_years:
                return 1.0
            elif resume_years >= job_years * 0.8:  # Within 80% of requirement
                return 0.8
            elif resume_years >= job_years * 0.6:  # Within 60% of requirement
                return 0.6
            else:
                return 0.3
        
        if job_level:
            level_requirements = {
                'entry': (0, 2),
                'mid': (3, 5),
                'senior': (6, 10),
                'executive': (10, float('inf'))
            }
            
            if job_level in level_requirements:
                min_years, max_years = level_requirements[job_level]
                if min_years <= resume_years <= max_years:
                    return 1.0
                elif resume_years >= min_years * 0.8:
                    return 0.8
                else:
                    return 0.4
        
        return 0.5  # Default neutral score
    
    async def _calculate_keyword_similarity(self, resume_keywords: List[str], 
                                          job_description: str) -> float:
        """Calculate keyword similarity using TF-IDF"""
        try:
            if not resume_keywords:
                return 0.0
            
            # Prepare texts
            resume_text = ' '.join(resume_keywords)
            job_text = self._clean_text(job_description)
            
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating keyword similarity: {e}")
            return 0.0
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for analysis"""
        # Convert to lowercase and remove extra whitespace
        text = re.sub(r'\s+', ' ', text.lower().strip())
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\-]', ' ', text)
        
        return text
    
    async def _generate_detailed_analysis(self, resume_analysis: Dict[str, Any],
                                        job_requirements: Dict[str, Any],
                                        match_scores: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed match analysis"""
        
        analysis = {
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "skill_gaps": [],
            "competitive_advantages": []
        }
        
        # Identify strengths
        if match_scores["categories"]["technical_skills"] >= 0.7:
            analysis["strengths"].append("Strong technical skill alignment")
        
        if match_scores["categories"]["experience"] >= 0.8:
            analysis["strengths"].append("Experience level matches requirements")
        
        if match_scores["categories"]["must_have"] >= 0.8:
            analysis["strengths"].append("Meets most critical requirements")
        
        # Identify weaknesses
        if match_scores["categories"]["technical_skills"] < 0.5:
            analysis["weaknesses"].append("Limited technical skill overlap")
        
        if match_scores["categories"]["experience"] < 0.6:
            analysis["weaknesses"].append("Experience level below requirements")
        
        if match_scores["categories"]["must_have"] < 0.7:
            analysis["weaknesses"].append("Missing some critical requirements")
        
        # Generate recommendations
        missing_tech = match_scores["requirements_missing"]["technical_skills"]
        if missing_tech:
            analysis["recommendations"].append(f"Consider highlighting experience with: {', '.join(missing_tech[:3])}")
        
        missing_must_have = match_scores["requirements_missing"]["must_have"]
        if missing_must_have:
            analysis["skill_gaps"] = missing_must_have
            analysis["recommendations"].append("Focus on addressing critical skill gaps in resume optimization")
        
        # Identify competitive advantages
        nice_to_have_met = match_scores["requirements_met"]["nice_to_have"]
        if nice_to_have_met:
            analysis["competitive_advantages"] = nice_to_have_met
        
        return analysis
    
    def _get_recommendation(self, overall_score: float) -> str:
        """Get application recommendation based on match score"""
        if overall_score >= 0.8:
            return "Highly recommended - Excellent match"
        elif overall_score >= 0.7:
            return "Recommended - Good match with minor gaps"
        elif overall_score >= 0.6:
            return "Consider applying - Moderate match, resume optimization recommended"
        elif overall_score >= 0.5:
            return "Marginal match - Significant resume optimization needed"
        else:
            return "Not recommended - Poor match for current profile"
    
    async def _save_match_result(self, job_id: str, match_result: Dict[str, Any]) -> None:
        """Save match result to file"""
        try:
            matches_file = self.config.data_dir / "job_matches.json"
            
            # Load existing matches
            matches = {}
            if matches_file.exists():
                with open(matches_file, 'r') as f:
                    matches = json.load(f)
            
            # Add new match
            matches[job_id] = match_result
            
            # Save updated matches
            with open(matches_file, 'w') as f:
                json.dump(matches, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving match result: {e}")
    
    async def get_match_history(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """Get match history for the specified period"""
        try:
            matches_file = self.config.data_dir / "job_matches.json"
            
            if not matches_file.exists():
                return []
            
            with open(matches_file, 'r') as f:
                matches = json.load(f)
            
            # Filter by date if needed
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            filtered_matches = []
            for job_id, match_data in matches.items():
                match_date = datetime.fromisoformat(match_data["matched_at"])
                if match_date >= cutoff_date:
                    filtered_matches.append({
                        "job_id": job_id,
                        **match_data
                    })
            
            # Sort by match date (newest first)
            filtered_matches.sort(key=lambda x: x["matched_at"], reverse=True)
            
            return filtered_matches
            
        except Exception as e:
            logger.error(f"Error getting match history: {e}")
            return []