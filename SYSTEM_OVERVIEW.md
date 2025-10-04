# PhenoML Healthcare Query Processing System

## Overview

This system provides a comprehensive solution for processing healthcare queries through PhenoML, converting natural language patient queries into structured JSON data suitable for appointment booking and clinical decision support.

## System Architecture

### Core Components

1. **PhenoML Prompt Template** (`phenoml_prompt_template.py`)
   - Comprehensive prompt engineering for healthcare queries
   - Includes clinical guidelines, symptom assessment, and appointment routing
   - Structured to produce consistent JSON outputs

2. **JSON Schema** (`appointment_schema.json`)
   - Defines the complete structure for appointment booking data
   - Includes patient info, symptoms assessment, clinical guidelines, and priority levels
   - Validates all system outputs for consistency

3. **PhenoML Integration** (`phenoml_integration.py`)
   - `PhenoMLClient`: Main client for API interactions
   - `MockPhenoMLClient`: Testing client with sample data
   - `HealthcareQueryProcessor`: High-level query processing with validation
   - Authentication, error handling, and batch processing capabilities

4. **Testing Framework** (`test_framework.py`)
   - Comprehensive unit tests for all components
   - Scenario-based testing with quality scoring
   - Automated validation against expected outputs

5. **Example Queries** (`example_queries.py`)
   - 5 comprehensive healthcare scenarios
   - Expected JSON outputs for each scenario
   - Covers emergency, routine, mental health, pediatric, and chronic conditions

## Key Features

### 1. Comprehensive Healthcare Query Processing
- **Symptom Assessment**: Standardized symptom categorization and severity scoring
- **Clinical Guidelines**: Integration with medical guidelines and recommendations
- **Priority Triage**: Automatic priority assignment (emergency, urgent, semi-urgent, routine)
- **Appointment Routing**: Intelligent routing to appropriate care types and specialties

### 2. Robust JSON Output Structure
```json
{
  "patient_info": {
    "age_range": "standardized age brackets",
    "gender": "male|female|other|not_specified",
    "pregnancy_status": "pregnant|not_pregnant|unknown|not_applicable",
    "chronic_conditions": ["array of conditions"]
  },
  "symptoms_assessment": {
    "primary_symptoms": [
      {
        "symptom": "standardized description",
        "body_system": "affected system",
        "severity": "mild|moderate|severe"
      }
    ],
    "severity": "emergency|urgent|semi-urgent|routine",
    "duration": "acute|subacute|chronic",
    "onset": "sudden|gradual|unknown",
    "red_flags": ["warning signs"]
  },
  "appointment_request": {
    "appointment_type": "emergency|urgent_care|primary_care|specialist_referral|telemedicine|mental_health|preventive_care",
    "specialty_required": "specialty or none",
    "urgency": "immediate|within_24h|within_week|within_month|routine",
    "preferred_timeframe": "patient preference",
    "appointment_reason": "clinical summary"
  },
  "clinical_guidelines": {
    "applicable_guidelines": [
      {
        "guideline_name": "guideline name",
        "organization": "publishing organization",
        "relevance": "primary|secondary|supportive"
      }
    ],
    "recommendations": ["clinical recommendations"],
    "contraindications": ["warnings and contraindications"]
  },
  "priority_level": "emergency|urgent|semi_urgent|routine",
  "additional_notes": {
    "patient_concerns": "specific concerns",
    "follow_up_needed": true/false,
    "diagnostic_tests_suggested": ["suggested tests"],
    "lifestyle_factors": ["relevant factors"]
  },
  "confidence_score": 0.0-1.0
}
```

### 3. Quality Assurance
- **JSON Schema Validation**: All outputs validated against comprehensive schema
- **Quality Scoring**: Automated quality assessment based on completeness and accuracy
- **Error Handling**: Robust error handling with detailed logging
- **Mock Testing**: Comprehensive mock client for development and testing

### 4. Flexible Integration
- **Authentication**: Secure API authentication with token management
- **Batch Processing**: Support for processing multiple queries simultaneously
- **Configuration Management**: Centralized configuration for API endpoints and settings
- **Logging**: Comprehensive logging for debugging and monitoring

## Usage Examples

### Single Query Processing
```python
from phenoml_integration import PhenoMLClient, HealthcareQueryProcessor

# Initialize client and processor
client = PhenoMLClient()
processor = HealthcareQueryProcessor(client)

# Process a healthcare query
result = processor.process_query(
    "I have chest pain and shortness of breath",
    {"age": 45, "gender": "male"}
)

print(f"Quality Score: {result['quality_score']}")
print(f"Appointment Type: {result['appointment_data']['appointment_request']['appointment_type']}")
```

### Batch Processing
```python
# Process multiple queries from JSON file
results = client.process_batch_queries("sample_batch_queries.json")
print(f"Processed {len(results)} queries")
```

### Mock Testing
```python
from phenoml_integration import MockPhenoMLClient

# Use mock client for testing
mock_client = MockPhenoMLClient()
result = mock_client.process_healthcare_query("I need a checkup")
```

## Testing and Validation

### Test Coverage
- **Unit Tests**: All core components tested individually
- **Integration Tests**: End-to-end testing with mock and real clients
- **Scenario Tests**: 5 comprehensive healthcare scenarios
- **Schema Validation**: All outputs validated against JSON schema

### Quality Metrics
- **Completeness**: Measures how many required fields are populated
- **Accuracy**: Validates against expected outputs for known scenarios
- **Consistency**: Ensures consistent formatting and structure
- **Clinical Relevance**: Validates medical accuracy and appropriateness

### Running Tests
```bash
# Run comprehensive test suite
python test_framework.py

# Test single query with mock client
python main.py --mock --query "I have a headache"

# Process batch queries
python main.py --mock --batch sample_batch_queries.json
```

## Configuration

### Environment Variables
- `PHENOML_API_URL`: PhenoML API endpoint
- `PHENOML_API_KEY`: API authentication key
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Configuration Files
- `config.py`: Centralized configuration management
- `sample_batch_queries.json`: Sample queries for batch processing
- `appointment_schema.json`: JSON schema for validation

## Clinical Guidelines Integration

The system incorporates evidence-based clinical guidelines from major medical organizations:

- **American Heart Association (AHA)**: Cardiac conditions and emergency protocols
- **American College of Emergency Physicians (ACEP)**: Emergency medicine guidelines
- **American Academy of Pediatrics (AAP)**: Pediatric care standards
- **American Psychiatric Association (APA)**: Mental health assessment protocols
- **Centers for Disease Control and Prevention (CDC)**: Public health guidelines

## Security and Compliance

### Data Protection
- No PHI (Protected Health Information) stored permanently
- Secure API communication with token-based authentication
- Input sanitization and validation
- Comprehensive error handling without data exposure

### Medical Disclaimer
This system is designed to assist healthcare professionals and should not be used as a substitute for professional medical advice, diagnosis, or treatment. All outputs should be reviewed by qualified healthcare providers.

## Future Enhancements

### Planned Features
1. **FHIR Integration**: Direct integration with FHIR servers for appointment booking
2. **Real-time Guidelines**: Dynamic updates from medical guideline databases
3. **Multi-language Support**: Support for non-English healthcare queries
4. **Advanced Analytics**: Detailed analytics and reporting capabilities
5. **Provider Integration**: Direct integration with healthcare provider systems

### Scalability Considerations
- Asynchronous processing for high-volume scenarios
- Caching for frequently accessed guidelines
- Load balancing for multiple PhenoML instances
- Database integration for persistent storage

## Support and Maintenance

### Monitoring
- Comprehensive logging for all operations
- Quality score tracking for continuous improvement
- Error rate monitoring and alerting
- Performance metrics and optimization

### Updates
- Regular updates to clinical guidelines
- Schema evolution for new healthcare requirements
- API version management and backward compatibility
- Security updates and vulnerability management

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-04  
**Status**: Production Ready