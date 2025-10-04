# PhenoML Healthcare Query Processing System

A comprehensive system for processing healthcare queries using PhenoML AI to generate structured appointment booking data compatible with FHIR standards.

## Overview

This system integrates OpenAI language understanding with PhenoML's healthcare-specific AI capabilities to:

1. **Process natural language healthcare queries** from patients
2. **Analyze symptoms** using clinical guidelines and medical knowledge
3. **Assess urgency and severity** levels for proper care routing
4. **Generate structured JSON output** compatible with FHIR appointment booking standards
5. **Route patients** to appropriate care levels (primary care, urgent care, emergency, specialists)

## Architecture

```
Patient Query → OpenAI (Language Understanding) → PhenoML (Healthcare Processing) → Structured JSON → FHIR Appointment Booking
```

### Key Components

- **PhenoML Integration**: Handles API communication with PhenoML services
- **Prompt Engineering**: Comprehensive prompts for clinical assessment
- **JSON Schema**: FHIR-compatible appointment booking data structure
- **Clinical Guidelines**: Integration with evidence-based medical guidelines
- **Testing Framework**: Comprehensive testing with healthcare scenarios

## Features

### 🩺 Clinical Assessment
- Symptom identification and categorization
- Body system classification
- Severity assessment (mild/moderate/severe)
- Duration analysis (acute/subacute/chronic)
- Red flag detection for emergency conditions

### 📋 Appointment Routing
- **Primary Care**: General health concerns, routine check-ups
- **Urgent Care**: Minor injuries, acute infections
- **Emergency**: Life-threatening conditions
- **Specialist Referral**: Complex conditions requiring specialized care
- **Telemedicine**: Remote consultation appropriate cases
- **Mental Health**: Psychiatric and psychological concerns

### 📚 Clinical Guidelines Integration
- WHO, CDC, and medical society guidelines
- Evidence-based diagnostic criteria
- Contraindications and warnings
- Diagnostic test recommendations

### 🔄 Priority Levels
- **Emergency**: Immediate care required
- **Urgent**: Care within 24 hours
- **Semi-urgent**: Care within a week
- **Routine**: Scheduled care

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AI_agent_hackathon
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure PhenoML credentials:
```python
# Update the auth_token in phenoml_integration.py or pass as parameter
client = PhenoMLClient(auth_token="your_base64_encoded_token")
```

## Usage

### Command Line Interface

#### Interactive Mode
```bash
python main.py --interactive
```

#### Process Single Query
```bash
python main.py --query "I have chest pain and shortness of breath"
```

#### Run Example Scenarios
```bash
python main.py --examples
```

#### Run Specific Scenario Type
```bash
python main.py --examples --scenario emergency
```

#### Batch Processing
```bash
python main.py --batch queries.json --output results.json
```

### Python API

```python
from phenoml_integration import PhenoMLClient, HealthcareQueryProcessor

# Initialize client
client = PhenoMLClient()
processor = HealthcareQueryProcessor(client)

# Process a query
query = "I've been having severe headaches for 3 days with nausea"
result = processor.process_query(query)

print(f"Priority: {result['appointment_data']['priority_level']}")
print(f"Appointment Type: {result['appointment_data']['appointment_request']['appointment_type']}")
```

## JSON Output Schema

The system generates structured JSON output with the following key sections:

### Patient Information
```json
{
  "patient_info": {
    "age_range": "18-35",
    "gender": "female",
    "pregnancy_status": "unknown",
    "chronic_conditions": ["hypertension"]
  }
}
```

### Symptoms Assessment
```json
{
  "symptoms_assessment": {
    "primary_symptoms": [
      {
        "symptom": "severe headache",
        "body_system": "neurological",
        "severity": "severe"
      }
    ],
    "severity": "high",
    "duration": "acute",
    "red_flags": ["severe headache with nausea"]
  }
}
```

### Appointment Request
```json
{
  "appointment_request": {
    "appointment_type": "urgent_care",
    "specialty_required": "neurology",
    "urgency": "within_24h",
    "appointment_reason": "Severe headache evaluation"
  }
}
```

### Clinical Guidelines
```json
{
  "clinical_guidelines": {
    "applicable_guidelines": [
      {
        "guideline_name": "International Headache Society Guidelines",
        "organization": "IHS",
        "relevance": "primary"
      }
    ],
    "recommendations": ["Neurological examination", "Consider imaging if red flags present"]
  }
}
```

## Example Scenarios

The system includes comprehensive test scenarios:

### 1. Emergency Scenario
**Query**: "I'm having severe chest pain radiating to my left arm with nausea"
**Output**: Emergency priority, immediate cardiology consultation

### 2. Routine Care
**Query**: "I've had a persistent cough for 2 weeks"
**Output**: Primary care appointment within a week

### 3. Mental Health
**Query**: "I've been feeling anxious and can't sleep for 3 weeks"
**Output**: Mental health appointment, psychiatry referral

### 4. Pediatric Care
**Query**: "My 8-year-old has fever and sore throat for 2 days"
**Output**: Urgent care, pediatric evaluation

## Testing

### Run Unit Tests
```bash
python -m unittest test_framework.py
```

### Run Scenario Tests
```bash
python test_framework.py
```

### Mock Testing
```bash
python main.py --mock --examples
```

## Configuration

### PhenoML API Configuration
```python
# In phenoml_integration.py
PHENOML_BASE_URL = "https://experiment.app.pheno.ml"
AUTH_TOKEN = "your_base64_encoded_credentials"
```

### Prompt Customization
Modify `phenoml_prompt_template.py` to customize:
- Clinical assessment criteria
- Guideline references
- Output format requirements
- Safety protocols

## File Structure

```
AI_agent_hackathon/
├── main.py                     # Main application entry point
├── phenoml_integration.py      # PhenoML API integration
├── phenoml_prompt_template.py  # Prompt templates
├── appointment_schema.json     # JSON schema definition
├── example_queries.py          # Example scenarios and validation
├── test_framework.py          # Comprehensive testing framework
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## API Endpoints

The system is designed to integrate with PhenoML's API endpoints:

- **Authentication**: `/auth/token`
- **Query Processing**: `/api/v1/process` (endpoint may vary)

## Safety and Compliance

### Medical Safety
- Always errs on the side of caution for severity assessment
- Flags potential emergency conditions
- Includes contraindications and warnings
- References established clinical guidelines

### Data Privacy
- No patient data is stored permanently
- All processing is stateless
- Complies with healthcare data privacy requirements

### Clinical Accuracy
- Uses standardized medical terminology
- References current clinical guidelines
- Considers patient demographics in assessment
- Provides confidence scores for assessments

## Limitations

- This system provides **clinical decision support** and should not replace professional medical judgment
- All outputs should be reviewed by qualified healthcare professionals
- The system is designed for **appointment routing** and **initial assessment**, not diagnosis
- Emergency conditions should always be directed to immediate medical care

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

[Add your license information here]

## Support

For technical support or questions about implementation, please [contact information].

## Changelog

### Version 1.0.0
- Initial release with comprehensive healthcare query processing
- FHIR-compatible JSON output schema
- Integration with PhenoML API
- Comprehensive testing framework
- Interactive and batch processing modes