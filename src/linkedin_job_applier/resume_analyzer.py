"""Resume analysis and keyword extraction"""

import logging
import re
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
import json

import PyPDF2
from docx import Document
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

from .config import Config

logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    """Analyze resume content and extract keywords/skills"""
    
    def __init__(self, config: Config):
        self.config = config
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set()
        self.tech_skills = set()
        self.soft_skills = set()
        self.resume_data: Optional[Dict[str, Any]] = None
        
    async def initialize(self) -> None:
        """Initialize NLTK data and skill databases"""
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            
            self.stop_words = set(stopwords.words('english'))
            
            # Load skill databases
            await self._load_skill_databases()
            
            logger.info("Resume analyzer initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing resume analyzer: {e}")
            raise
    
    async def _load_skill_databases(self) -> None:
        """Load technical and soft skills databases"""
        # Technical skills (programming languages, frameworks, tools)
        self.tech_skills = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
            'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
            'django', 'flask', 'spring', 'laravel', 'rails',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'cassandra', 'dynamodb', 'sqlite',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'terraform', 'ansible', 'git', 'github', 'gitlab',
            
            # Data Science & ML
            'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch',
            'keras', 'spark', 'hadoop', 'tableau', 'powerbi',
            
            # Other Tools
            'linux', 'unix', 'bash', 'powershell', 'vim', 'vscode',
            'intellij', 'eclipse', 'jira', 'confluence'
        }
        
        # Soft skills
        self.soft_skills = {
            'leadership', 'communication', 'teamwork', 'problem-solving',
            'analytical', 'creative', 'adaptable', 'organized', 'detail-oriented',
            'collaborative', 'innovative', 'strategic', 'mentoring', 'coaching',
            'project management', 'time management', 'critical thinking',
            'decision making', 'conflict resolution', 'presentation skills'
        }
    
    async def analyze_resume(self, resume_path: str) -> Dict[str, Any]:
        """Analyze resume and extract key information"""
        try:
            resume_file = Path(resume_path)
            
            if not resume_file.exists():
                return {"error": f"Resume file not found: {resume_path}"}
            
            # Extract text from resume
            text = await self._extract_text_from_file(resume_file)
            
            if not text:
                return {"error": "Could not extract text from resume"}
            
            # Analyze the text
            analysis = await self._analyze_text(text)
            
            # Store analysis results
            self.resume_data = {
                "file_path": str(resume_file),
                "text": text,
                "analysis": analysis,
                "analyzed_at": pd.Timestamp.now().isoformat()
            }
            
            # Save analysis to cache
            await self._save_resume_analysis()
            
            return {
                "success": True,
                "file_path": str(resume_file),
                "analysis": analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing resume: {e}")
            return {"error": str(e)}
    
    async def _extract_text_from_file(self, file_path: Path) -> str:
        """Extract text from PDF, DOCX, or TXT file"""
        try:
            if file_path.suffix.lower() == '.pdf':
                return await self._extract_from_pdf(file_path)
            elif file_path.suffix.lower() in ['.docx', '.doc']:
                return await self._extract_from_docx(file_path)
            elif file_path.suffix.lower() == '.txt':
                return await self._extract_from_txt(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            return ""
    
    async def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            raise
        
        return text.strip()
    
    async def _extract_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            logger.error(f"Error reading DOCX: {e}")
            raise
    
    async def _extract_from_txt(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text.strip()
        except Exception as e:
            logger.error(f"Error reading TXT: {e}")
            raise
    
    async def _analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze resume text and extract key information"""
        # Clean and preprocess text
        cleaned_text = self._clean_text(text)
        
        # Extract different types of information
        analysis = {
            "word_count": len(text.split()),
            "sentences": len(sent_tokenize(text)),
            "contact_info": self._extract_contact_info(text),
            "technical_skills": self._extract_technical_skills(cleaned_text),
            "soft_skills": self._extract_soft_skills(cleaned_text),
            "experience_years": self._extract_experience_years(text),
            "education": self._extract_education(text),
            "keywords": self._extract_keywords(cleaned_text),
            "sections": self._identify_sections(text),
            "key_phrases": self._extract_key_phrases(cleaned_text)
        }
        
        return analysis
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = text.lower().strip()
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\-\+\#]', ' ', text)
        
        return text
    
    def _extract_contact_info(self, text: str) -> Dict[str, Optional[str]]:
        """Extract contact information from resume"""
        contact_info = {
            "email": None,
            "phone": None,
            "linkedin": None,
            "github": None,
            "website": None
        }
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info["email"] = email_match.group()
        
        # Phone
        phone_pattern = r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact_info["phone"] = phone_match.group()
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact_info["linkedin"] = linkedin_match.group()
        
        # GitHub
        github_pattern = r'github\.com/[\w-]+'
        github_match = re.search(github_pattern, text, re.IGNORECASE)
        if github_match:
            contact_info["github"] = github_match.group()
        
        return contact_info
    
    def _extract_technical_skills(self, text: str) -> List[str]:
        """Extract technical skills from resume"""
        found_skills = []
        
        # Tokenize text
        tokens = word_tokenize(text)
        
        # Look for technical skills
        for skill in self.tech_skills:
            skill_lower = skill.lower()
            if skill_lower in text or any(skill_lower in token for token in tokens):
                found_skills.append(skill)
        
        # Look for version numbers and frameworks
        tech_patterns = [
            r'\b\w+\.js\b',  # JavaScript frameworks
            r'\b\w+\s+\d+(\.\d+)?\b',  # Versions
            r'\b[A-Z]{2,}\b',  # Acronyms
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text)
            found_skills.extend(matches)
        
        return list(set(found_skills))
    
    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills from resume"""
        found_skills = []
        
        for skill in self.soft_skills:
            if skill.lower() in text:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_experience_years(self, text: str) -> Optional[int]:
        """Extract years of experience from resume"""
        # Look for patterns like "5 years of experience", "5+ years", etc.
        patterns = [
            r'(\d+)\+?\s*years?\s*of\s*experience',
            r'(\d+)\+?\s*years?\s*experience',
            r'(\d+)\+?\s*yrs?\s*experience',
            r'experience.*?(\d+)\+?\s*years?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education = []
        
        # Common degree patterns
        degree_patterns = [
            r'\b(bachelor|master|phd|doctorate|associate).*?(degree|of|in)\s+([^\n]+)',
            r'\b(b\.?s\.?|m\.?s\.?|m\.?a\.?|ph\.?d\.?|b\.?a\.?)\s+([^\n]+)',
            r'\b(university|college|institute)\s+([^\n]+)',
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            education.extend([' '.join(match) for match in matches])
        
        return education
    
    def _extract_keywords(self, text: str, max_keywords: int = 20) -> List[str]:
        """Extract important keywords using TF-IDF"""
        try:
            # Tokenize and remove stop words
            tokens = word_tokenize(text)
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                     if token.isalpha() and token not in self.stop_words and len(token) > 2]
            
            if not tokens:
                return []
            
            # Use TF-IDF to find important terms
            vectorizer = TfidfVectorizer(max_features=max_keywords, ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform([' '.join(tokens)])
            
            feature_names = vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Get top keywords
            keyword_scores = list(zip(feature_names, tfidf_scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            return [keyword for keyword, score in keyword_scores[:max_keywords]]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def _identify_sections(self, text: str) -> List[str]:
        """Identify resume sections"""
        sections = []
        
        section_patterns = [
            r'\b(summary|objective|profile)\b',
            r'\b(experience|employment|work history)\b',
            r'\b(education|academic)\b',
            r'\b(skills|technical skills|competencies)\b',
            r'\b(projects|portfolio)\b',
            r'\b(certifications|certificates)\b',
            r'\b(awards|achievements|honors)\b',
            r'\b(publications|papers)\b',
            r'\b(references|contact)\b',
        ]
        
        for pattern in section_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                sections.append(re.search(pattern, text, re.IGNORECASE).group(1))
        
        return sections
    
    def _extract_key_phrases(self, text: str, max_phrases: int = 10) -> List[str]:
        """Extract key phrases from resume"""
        try:
            # Use TF-IDF with n-grams to find key phrases
            vectorizer = TfidfVectorizer(
                max_features=max_phrases,
                ngram_range=(2, 4),
                stop_words='english'
            )
            
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Get top phrases
            phrase_scores = list(zip(feature_names, tfidf_scores))
            phrase_scores.sort(key=lambda x: x[1], reverse=True)
            
            return [phrase for phrase, score in phrase_scores[:max_phrases]]
            
        except Exception as e:
            logger.error(f"Error extracting key phrases: {e}")
            return []
    
    async def _save_resume_analysis(self) -> None:
        """Save resume analysis to cache file"""
        try:
            if self.resume_data:
                cache_file = self.config.data_dir / "resume_analysis.json"
                with open(cache_file, 'w') as f:
                    json.dump(self.resume_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving resume analysis: {e}")
    
    async def get_resume_data(self) -> Optional[Dict[str, Any]]:
        """Get current resume analysis data"""
        if not self.resume_data:
            # Try to load from cache
            try:
                cache_file = self.config.data_dir / "resume_analysis.json"
                if cache_file.exists():
                    with open(cache_file, 'r') as f:
                        self.resume_data = json.load(f)
            except Exception as e:
                logger.error(f"Error loading resume analysis cache: {e}")
        
        return self.resume_data
    
    def get_skills_summary(self) -> Dict[str, Any]:
        """Get summary of extracted skills"""
        if not self.resume_data:
            return {"error": "No resume analysis available"}
        
        analysis = self.resume_data.get("analysis", {})
        
        return {
            "technical_skills": analysis.get("technical_skills", []),
            "soft_skills": analysis.get("soft_skills", []),
            "total_skills": len(analysis.get("technical_skills", [])) + len(analysis.get("soft_skills", [])),
            "keywords": analysis.get("keywords", []),
            "key_phrases": analysis.get("key_phrases", [])
        }