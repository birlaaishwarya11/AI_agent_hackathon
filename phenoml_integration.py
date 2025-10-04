"""
PhenoML Integration Module
This module handles the integration with PhenoML API for healthcare query processing.
"""

import requests
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import base64

from phenoml_prompt_template import create_phenoml_prompt, create_simple_phenoml_prompt
from example_queries import validate_json_output

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PhenoMLClient:
    """
    Client for interacting with PhenoML API for healthcare query processing.
    """
    
    def __init__(self, base_url: str = "https://experiment.app.pheno.ml", 
                 auth_token: str = None):
        """
        Initialize PhenoML client.
        
        Args:
            base_url (str): Base URL for PhenoML API
            auth_token (str): Authentication token (base64 encoded)
        """
        self.base_url = base_url
        self.auth_token = auth_token or "WW91Z09FTDN5dzljc1lIdkFFMF80UTpRM1lQVFZPanloeU1KZWY4T2ZndW9n"
        self.session = requests.Session()
        self.access_token = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with PhenoML API and get access token.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            url = f"{self.base_url}/auth/token"
            headers = {
                "accept": "application/json",
                "authorization": f"Basic {self.auth_token}"
            }
            
            response = self.session.post(url, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            
            if self.access_token:
                logger.info("Successfully authenticated with PhenoML API")
                return True
            else:
                logger.error("No access token received from authentication")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication failed: {e}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse authentication response: {e}")
            return False
    
    def process_healthcare_query(self, patient_query: str, 
                               additional_context: str = "",
                               use_simple_prompt: bool = False) -> Optional[Dict[str, Any]]:
        """
        Process a healthcare query using PhenoML API.
        
        Args:
            patient_query (str): The patient's healthcare query
            additional_context (str): Optional additional context
            use_simple_prompt (bool): Whether to use simplified prompt
            
        Returns:
            Optional[Dict[str, Any]]: Structured appointment booking data or None if failed
        """
        if not self.access_token and not self.authenticate():
            logger.error("Cannot process query without authentication")
            return None
        
        try:
            # Create the prompt
            logger.debug("Creating prompt...")
            if use_simple_prompt:
                prompt = create_simple_phenoml_prompt(patient_query)
            else:
                prompt = create_phenoml_prompt(patient_query, additional_context)
            logger.debug("Prompt created successfully")
            
            # Make API call to PhenoML
            logger.debug("Making API call...")
            response_data = self._call_phenoml_api(prompt)
            logger.debug("API call completed")
            
            if response_data:
                # Parse and validate the response
                logger.debug("Parsing response...")
                parsed_response = self._parse_response(response_data)
                logger.debug("Response parsed")
                
                if parsed_response:
                    try:
                        logger.debug("Validating JSON output...")
                        if validate_json_output(parsed_response):
                            logger.info("Successfully processed healthcare query")
                            return parsed_response
                        else:
                            logger.error("Invalid response format from PhenoML - missing required fields")
                            logger.debug(f"Response keys: {list(parsed_response.keys()) if isinstance(parsed_response, dict) else 'Not a dict'}")
                            return None
                    except Exception as validation_error:
                        logger.error(f"Error validating JSON output: {validation_error}")
                        logger.debug(f"Parsed response: {parsed_response}")
                        return None
                else:
                    logger.error("Failed to parse response from PhenoML")
                    return None
            else:
                logger.error("No response received from PhenoML API")
                return None
                
        except Exception as e:
            logger.error(f"Error processing healthcare query: {e}")
            import traceback
            logger.debug(f"Full traceback: {traceback.format_exc()}")
            return None
    
    def _call_phenoml_api(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Make API call to PhenoML with the formatted prompt.
        
        Args:
            prompt (str): The formatted prompt for PhenoML
            
        Returns:
            Optional[Dict[str, Any]]: API response or None if failed
        """
        try:
            # This is a placeholder for the actual PhenoML API endpoint
            # You'll need to replace this with the correct endpoint and parameters
            url = f"{self.base_url}/api/v1/process"  # Replace with actual endpoint
            
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.access_token}",
                "content-type": "application/json"
            }
            
            payload = {
                "prompt": prompt,
                "model": "healthcare-assistant",  # Replace with actual model name
                "max_tokens": 2000,
                "temperature": 0.1,  # Low temperature for consistent medical responses
                "response_format": "json"
            }
            
            response = self.session.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse API response: {e}")
            return None
    
    def _parse_response(self, response_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse the response from PhenoML API.
        
        Args:
            response_data (Dict[str, Any]): Raw response from API
            
        Returns:
            Optional[Dict[str, Any]]: Parsed appointment booking data
        """
        try:
            logger.debug(f"Raw response data: {response_data}")
            
            # Extract the actual response content
            # This will depend on the actual PhenoML API response format
            if "choices" in response_data and len(response_data["choices"]) > 0:
                content = response_data["choices"][0].get("message", {}).get("content", "")
            elif "response" in response_data:
                content = response_data["response"]
            else:
                content = str(response_data)
            
            logger.debug(f"Extracted content: {repr(content[:200])}")
            
            # Try to parse JSON from the content
            if isinstance(content, str):
                # Clean the content first
                content = content.strip()
                
                # Look for JSON in the content
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                
                if start_idx != -1 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    logger.debug(f"Extracted JSON string: {repr(json_str[:200])}")
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError as json_error:
                        logger.error(f"JSON decode error: {json_error}")
                        logger.debug(f"Failed JSON string: {repr(json_str)}")
                        return None
                else:
                    # Try parsing the entire content as JSON
                    logger.debug("Trying to parse entire content as JSON")
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError as json_error:
                        logger.error(f"JSON decode error on full content: {json_error}")
                        logger.debug(f"Failed content: {repr(content)}")
                        return None
            elif isinstance(content, dict):
                logger.debug("Content is already a dict")
                return content
            
            logger.error("Could not extract JSON from response")
            return None
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Content that failed to parse: {repr(content[:500])}")
            return None
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            return None
    
    def batch_process_queries(self, queries: list) -> list:
        """
        Process multiple healthcare queries in batch.
        
        Args:
            queries (list): List of query dictionaries with 'query' and optional 'context'
            
        Returns:
            list: List of processed results
        """
        results = []
        
        for i, query_data in enumerate(queries):
            logger.info(f"Processing query {i+1}/{len(queries)}")
            
            query = query_data.get("query", "")
            context = query_data.get("context", "")
            
            result = self.process_healthcare_query(query, context)
            
            results.append({
                "query": query,
                "result": result,
                "processed_at": datetime.now().isoformat(),
                "success": result is not None
            })
        
        return results

class HealthcareQueryProcessor:
    """
    High-level processor for healthcare queries with additional validation and formatting.
    """
    
    def __init__(self, phenoml_client: PhenoMLClient):
        """
        Initialize the processor with a PhenoML client.
        
        Args:
            phenoml_client (PhenoMLClient): Configured PhenoML client
        """
        self.client = phenoml_client
    
    def process_query(self, patient_query: str, 
                     patient_demographics: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a healthcare query with additional validation and formatting.
        
        Args:
            patient_query (str): The patient's healthcare query
            patient_demographics (Dict[str, Any]): Optional patient demographic information
            
        Returns:
            Dict[str, Any]: Processed result with metadata
        """
        # Prepare additional context from demographics
        additional_context = ""
        if patient_demographics:
            context_parts = []
            if "age" in patient_demographics:
                context_parts.append(f"Patient age: {patient_demographics['age']}")
            if "gender" in patient_demographics:
                context_parts.append(f"Gender: {patient_demographics['gender']}")
            if "medical_history" in patient_demographics:
                context_parts.append(f"Medical history: {patient_demographics['medical_history']}")
            
            additional_context = "; ".join(context_parts)
        
        # Process the query
        result = self.client.process_healthcare_query(patient_query, additional_context)
        
        # Add metadata
        processed_result = {
            "original_query": patient_query,
            "patient_demographics": patient_demographics,
            "processed_at": datetime.now().isoformat(),
            "success": result is not None,
            "appointment_data": result
        }
        
        # Add quality score based on completeness
        if result:
            processed_result["quality_score"] = self._calculate_quality_score(result)
        
        return processed_result
    
    def _calculate_quality_score(self, appointment_data: Dict[str, Any]) -> float:
        """
        Calculate a quality score for the processed appointment data.
        
        Args:
            appointment_data (Dict[str, Any]): The processed appointment data
            
        Returns:
            float: Quality score between 0 and 1
        """
        score = 0.0
        max_score = 0.0
        
        # Check completeness of required fields
        required_fields = [
            "patient_info", "symptoms_assessment", "appointment_request",
            "clinical_guidelines", "priority_level"
        ]
        
        for field in required_fields:
            max_score += 1.0
            if field in appointment_data and appointment_data[field]:
                score += 1.0
        
        # Check for confidence score
        if "confidence_score" in appointment_data:
            max_score += 1.0
            confidence = appointment_data["confidence_score"]
            if isinstance(confidence, (int, float)) and 0 <= confidence <= 1:
                score += confidence
        
        # Check for clinical guidelines
        if "clinical_guidelines" in appointment_data:
            guidelines = appointment_data["clinical_guidelines"]
            if "applicable_guidelines" in guidelines and guidelines["applicable_guidelines"]:
                score += 0.5
            if "recommendations" in guidelines and guidelines["recommendations"]:
                score += 0.5
            max_score += 1.0
        
        return score / max_score if max_score > 0 else 0.0

class MockPhenoMLClient(PhenoMLClient):
    """
    Mock client for testing without actual API calls.
    """
    
    def __init__(self):
        """Initialize mock client."""
        super().__init__()
        self.access_token = "mock_token"
    
    def authenticate(self) -> bool:
        """Mock authentication."""
        return True
    
    def _call_phenoml_api(self, prompt: str) -> Dict[str, Any]:
        """
        Mock API call that returns a sample response.
        
        Args:
            prompt (str): The prompt (unused in mock)
            
        Returns:
            Dict[str, Any]: Mock API response
        """
        # Import here to avoid circular import
        try:
            from example_queries import EXAMPLE_QUERIES
            sample_output = EXAMPLE_QUERIES[0]["expected_output"]
        except ImportError:
            # Fallback sample output if import fails
            sample_output = {
                "patient_info": {
                    "age_range": "18-35",
                    "gender": "not_specified",
                    "pregnancy_status": "unknown",
                    "chronic_conditions": []
                },
                "symptoms_assessment": {
                    "primary_symptoms": [
                        {
                            "symptom": "chest pain",
                            "body_system": "cardiovascular",
                            "severity": "severe"
                        }
                    ],
                    "severity": "high",
                    "duration": "acute",
                    "onset": "sudden",
                    "red_flags": ["chest pain"]
                },
                "appointment_request": {
                    "appointment_type": "emergency",
                    "specialty_required": "cardiology",
                    "urgency": "immediate",
                    "appointment_reason": "Chest pain evaluation"
                },
                "clinical_guidelines": {
                    "applicable_guidelines": [
                        {
                            "guideline_name": "AHA Guidelines",
                            "organization": "American Heart Association",
                            "relevance": "primary"
                        }
                    ],
                    "recommendations": ["Immediate cardiac evaluation"],
                    "contraindications": []
                },
                "priority_level": "emergency",
                "additional_notes": {
                    "patient_concerns": "Chest pain",
                    "follow_up_needed": True,
                    "diagnostic_tests_suggested": ["ECG", "Troponin"],
                    "lifestyle_factors": []
                },
                "confidence_score": 0.9
            }
        
        # Return a mock response that looks like a typical LLM API response
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(sample_output, indent=2)
                    }
                }
            ]
        }
        return mock_response

# Example usage and testing functions
def test_phenoml_integration():
    """
    Test the PhenoML integration with example queries.
    """
    client = PhenoMLClient()
    processor = HealthcareQueryProcessor(client)
    
    # Test authentication
    if not client.authenticate():
        logger.error("Authentication failed - cannot run tests")
        return
    
    # Test with a simple query
    test_query = "I have a headache and fever for 2 days"
    result = processor.process_query(test_query)
    
    print("Test Result:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_phenoml_integration()