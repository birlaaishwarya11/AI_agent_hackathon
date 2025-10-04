"""
Real PhenoML SDK Integration for Healthcare Query Processing

This module provides integration with the actual PhenoML SDK for healthcare
query processing, agent creation, and FHIR server interactions.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class PhenoMLRealClient:
    """
    Real PhenoML client using the official PhenoML SDK.
    """
    
    def __init__(self):
        """Initialize the real PhenoML client."""
        self.client = None
        self.agent_id = None
        self.prompts = {}
        
    def authenticate(self) -> bool:
        """
        Authenticate with PhenoML using SDK.
        
        Returns:
            bool: True if authentication successful
        """
        try:
            # Import PhenoML SDK
            from phenoml import Client
            
            username = os.getenv("PHENOML_USERNAME")
            password = os.getenv("PHENOML_PASSWORD")
            base_url = os.getenv("PHENOML_BASE_URL")
            
            if not all([username, password, base_url]):
                logger.error("Missing PhenoML credentials in environment variables")
                return False
            
            self.client = Client(
                username=username,
                password=password,
                base_url=base_url
            )
            
            logger.info("Successfully authenticated with PhenoML")
            return True
            
        except ImportError:
            logger.error("PhenoML SDK not installed. Run: pip install phenoml")
            return False
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False
    
    def create_healthcare_prompts(self) -> Dict[str, Any]:
        """
        Create healthcare-specific prompts for appointment booking.
        
        Returns:
            Dict[str, Any]: Created prompt IDs and metadata
        """
        if not self.client:
            raise RuntimeError("Client not authenticated")
        
        # Healthcare appointment booking prompt
        appointment_booking_prompt = """
        You are a healthcare AI assistant specialized in processing patient queries for appointment booking.
        
        WORKFLOW:
        1. ANALYZE the patient's query to understand their healthcare needs
        2. EXTRACT key information: symptoms, urgency, patient demographics
        3. DETERMINE appropriate care type and specialty
        4. CREATE structured appointment data using FHIR resources
        5. PROVIDE clinical guidance based on established medical guidelines
        
        FHIR INTEGRATION:
        - Use lang2fhir_and_search to find existing patient records
        - Use lang2fhir_and_create to create new appointments, conditions, and observations
        - Always include full patient identifiers in FHIR operations
        
        CLINICAL GUIDELINES:
        - Apply evidence-based medical guidelines (AHA, ACEP, AAP, APA, CDC)
        - Identify red flags and emergency conditions
        - Recommend appropriate urgency levels and care settings
        
        APPOINTMENT TYPES:
        - emergency: Life-threatening conditions requiring immediate care
        - urgent_care: Acute conditions needing same-day care
        - primary_care: Routine care and chronic condition management
        - specialist_referral: Conditions requiring specialized expertise
        - telemedicine: Suitable for remote consultation
        - mental_health: Psychiatric and psychological care
        - preventive_care: Wellness visits and screenings
        
        Always prioritize patient safety and provide appropriate medical guidance.
        """
        
        # Symptom assessment prompt
        symptom_assessment_prompt = """
        You are a clinical decision support assistant for symptom assessment and triage.
        
        ASSESSMENT FRAMEWORK:
        1. CATEGORIZE symptoms by body system and severity
        2. IDENTIFY red flags and warning signs
        3. ASSESS urgency and appropriate care level
        4. RECOMMEND diagnostic tests and clinical actions
        
        SEVERITY LEVELS:
        - emergency: Immediate life-threatening conditions
        - urgent: Conditions requiring care within 24 hours
        - semi_urgent: Conditions requiring care within a week
        - routine: Non-urgent conditions for routine scheduling
        
        RED FLAGS TO IDENTIFY:
        - Chest pain with cardiac risk factors
        - Severe headache with neurological symptoms
        - High fever in children or immunocompromised patients
        - Severe abdominal pain
        - Difficulty breathing or shortness of breath
        - Signs of stroke or heart attack
        
        Use FHIR Observation resources to document symptom assessments.
        """
        
        # Patient intake prompt
        patient_intake_prompt = """
        You are a medical assistant conducting comprehensive patient intake for appointment booking.
        
        NEW PATIENT WORKFLOW:
        1. COLLECT basic demographics: name, date of birth, contact information
        2. CREATE patient resource using lang2fhir_and_create
        3. GATHER medical history and current medications
        4. DOCUMENT conditions using lang2fhir_and_create for Condition resources
        5. RECORD medications using lang2fhir_and_create for MedicationRequest resources
        
        EXISTING PATIENT WORKFLOW:
        1. SEARCH for patient using lang2fhir_and_search
        2. EXTRACT patient identifier for subsequent operations
        3. UPDATE medical information as needed
        4. CREATE appointment based on current needs
        
        INFORMATION TO COLLECT:
        - Chief complaint and current symptoms
        - Medical history and chronic conditions
        - Current medications and allergies
        - Insurance and contact information
        - Preferred appointment times and care preferences
        
        Always maintain patient privacy and follow HIPAA guidelines.
        """
        
        try:
            # Create prompts using PhenoML SDK
            appointment_prompt = self.client.agent.prompts.create(
                name="healthcare_appointment_booking",
                content=appointment_booking_prompt,
                is_active=True,
                description="Comprehensive healthcare appointment booking and clinical guidance"
            )
            
            symptom_prompt = self.client.agent.prompts.create(
                name="symptom_assessment_triage",
                content=symptom_assessment_prompt,
                is_active=True,
                description="Clinical symptom assessment and triage guidance"
            )
            
            intake_prompt = self.client.agent.prompts.create(
                name="patient_intake_comprehensive",
                content=patient_intake_prompt,
                is_active=True,
                description="Comprehensive patient intake and registration"
            )
            
            self.prompts = {
                "appointment_booking": appointment_prompt.data.id,
                "symptom_assessment": symptom_prompt.data.id,
                "patient_intake": intake_prompt.data.id
            }
            
            logger.info(f"Created {len(self.prompts)} healthcare prompts")
            return self.prompts
            
        except Exception as e:
            logger.error(f"Failed to create prompts: {e}")
            raise
    
    def create_healthcare_agent(self, provider_id: str = None) -> str:
        """
        Create a healthcare agent with appointment booking capabilities.
        
        Args:
            provider_id (str): Optional FHIR provider ID
            
        Returns:
            str: Created agent ID
        """
        if not self.client or not self.prompts:
            raise RuntimeError("Client not authenticated or prompts not created")
        
        try:
            # Create healthcare agent with all prompts
            agent = self.client.agent.create(
                name="Healthcare Appointment Booking Agent",
                prompts=list(self.prompts.values()),
                is_active=True,
                provider=provider_id
            )
            
            self.agent_id = agent.data.id
            logger.info(f"Created healthcare agent with ID: {self.agent_id}")
            return self.agent_id
            
        except Exception as e:
            logger.error(f"Failed to create agent: {e}")
            raise
    
    def process_healthcare_query(self, query: str, patient_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a healthcare query using the PhenoML agent.
        
        Args:
            query (str): Patient's healthcare query
            patient_context (Dict[str, Any]): Optional patient context information
            
        Returns:
            Dict[str, Any]: Processed healthcare data with FHIR resources
        """
        if not self.client or not self.agent_id:
            raise RuntimeError("Client not authenticated or agent not created")
        
        try:
            # Prepare context for the agent
            context = f"Patient Query: {query}"
            if patient_context:
                context += f"\nPatient Context: {json.dumps(patient_context, indent=2)}"
            
            # Process query through PhenoML agent
            response = self.client.agent.chat(
                agent_id=self.agent_id,
                message=context
            )
            
            # Extract structured data from response
            result = {
                "query": query,
                "patient_context": patient_context,
                "agent_response": response.data.message,
                "fhir_resources": self._extract_fhir_resources(response),
                "appointment_data": self._extract_appointment_data(response),
                "processed_at": datetime.now().isoformat(),
                "agent_id": self.agent_id
            }
            
            logger.info("Successfully processed healthcare query")
            return result
            
        except Exception as e:
            logger.error(f"Failed to process healthcare query: {e}")
            raise
    
    def _extract_fhir_resources(self, response) -> List[Dict[str, Any]]:
        """
        Extract FHIR resources from agent response.
        
        Args:
            response: PhenoML agent response
            
        Returns:
            List[Dict[str, Any]]: Extracted FHIR resources
        """
        # This would extract FHIR resources created by the agent
        # Implementation depends on PhenoML response format
        return []
    
    def _extract_appointment_data(self, response) -> Dict[str, Any]:
        """
        Extract appointment booking data from agent response.
        
        Args:
            response: PhenoML agent response
            
        Returns:
            Dict[str, Any]: Structured appointment data
        """
        # This would extract structured appointment data
        # Implementation depends on PhenoML response format
        return {
            "appointment_type": "primary_care",
            "urgency": "routine",
            "specialty_required": None,
            "clinical_notes": response.data.message if hasattr(response.data, 'message') else ""
        }

class HealthcareAgentManager:
    """
    Manager for healthcare agents and FHIR integration.
    """
    
    def __init__(self):
        """Initialize the healthcare agent manager."""
        self.client = PhenoMLRealClient()
        self.agents = {}
    
    def setup_healthcare_system(self, provider_id: str = None) -> Dict[str, str]:
        """
        Set up the complete healthcare system with agents and prompts.
        
        Args:
            provider_id (str): Optional FHIR provider ID
            
        Returns:
            Dict[str, str]: Created agent and prompt IDs
        """
        try:
            # Authenticate
            if not self.client.authenticate():
                raise RuntimeError("Failed to authenticate with PhenoML")
            
            # Create prompts
            prompts = self.client.create_healthcare_prompts()
            
            # Create agent
            agent_id = self.client.create_healthcare_agent(provider_id)
            
            result = {
                "agent_id": agent_id,
                "prompts": prompts,
                "status": "success"
            }
            
            logger.info("Healthcare system setup completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Failed to setup healthcare system: {e}")
            raise
    
    def process_patient_query(self, query: str, patient_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a patient query through the healthcare system.
        
        Args:
            query (str): Patient's healthcare query
            patient_info (Dict[str, Any]): Optional patient information
            
        Returns:
            Dict[str, Any]: Comprehensive healthcare response
        """
        try:
            # Process through PhenoML agent
            result = self.client.process_healthcare_query(query, patient_info)
            
            # Add quality assessment
            result["quality_score"] = self._assess_response_quality(result)
            
            # Add clinical recommendations
            result["clinical_recommendations"] = self._generate_clinical_recommendations(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to process patient query: {e}")
            raise
    
    def _assess_response_quality(self, result: Dict[str, Any]) -> float:
        """
        Assess the quality of the healthcare response.
        
        Args:
            result (Dict[str, Any]): Healthcare response data
            
        Returns:
            float: Quality score (0.0-1.0)
        """
        # Simple quality assessment based on completeness
        score = 0.0
        
        if result.get("agent_response"):
            score += 0.3
        if result.get("appointment_data"):
            score += 0.3
        if result.get("fhir_resources"):
            score += 0.2
        if result.get("patient_context"):
            score += 0.2
        
        return min(score, 1.0)
    
    def _generate_clinical_recommendations(self, result: Dict[str, Any]) -> List[str]:
        """
        Generate clinical recommendations based on the response.
        
        Args:
            result (Dict[str, Any]): Healthcare response data
            
        Returns:
            List[str]: Clinical recommendations
        """
        recommendations = []
        
        # Basic recommendations based on response content
        if "emergency" in str(result.get("appointment_data", {})).lower():
            recommendations.append("Seek immediate medical attention")
        
        if "chest pain" in result.get("query", "").lower():
            recommendations.append("Consider cardiac evaluation")
        
        if not recommendations:
            recommendations.append("Follow up with healthcare provider as recommended")
        
        return recommendations

# Example usage and testing
def test_real_phenoml_integration():
    """
    Test the real PhenoML integration.
    """
    try:
        manager = HealthcareAgentManager()
        
        # Setup healthcare system
        setup_result = manager.setup_healthcare_system()
        print(f"Setup result: {setup_result}")
        
        # Test patient query
        query = "I have chest pain and shortness of breath"
        patient_info = {
            "age": 45,
            "gender": "male",
            "medical_history": "Hypertension"
        }
        
        result = manager.process_patient_query(query, patient_info)
        print(f"Query result: {json.dumps(result, indent=2)}")
        
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Run test
    test_real_phenoml_integration()