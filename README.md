# PhenoML Healthcare Query Processing System

A comprehensive system for processing healthcare queries through PhenoML, converting natural language patient queries into structured JSON data suitable for appointment booking and clinical decision support with FHIR integration.

## 🏥 Overview

This system provides two integration approaches:
1. **Mock System**: For development, testing, and demonstration
2. **Real PhenoML SDK**: For production use with actual PhenoML agents and FHIR servers

## ✨ Features

- **Comprehensive Healthcare Query Processing**: Converts natural language patient queries into structured appointment booking data
- **Real PhenoML SDK Integration**: Uses official PhenoML SDK for agent creation and FHIR operations
- **Clinical Guidelines Integration**: Incorporates evidence-based medical guidelines from major healthcare organizations
- **FHIR Compatibility**: Direct FHIR server integration for patient records, appointments, and clinical data
- **Quality Assurance**: Automated quality scoring and validation
- **Flexible Integration**: Support for both mock testing and real PhenoML API integration
- **Batch Processing**: Process multiple queries simultaneously
- **Interactive Mode**: Real-time query processing interface
- **Comprehensive Testing**: Unit tests, integration tests, and scenario-based validation

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/birlaaishwarya11/AI_agent_hackathon.git
cd AI_agent_hackathon

# Install dependencies
pip install -r requirements.txt

# For real PhenoML integration, ensure phenoml SDK is installed
pip install phenoml
```

### Environment Setup

```bash
# Copy environment template
cp .env.template .env

# Edit .env with your PhenoML credentials
# PHENOML_USERNAME=your_username
# PHENOML_PASSWORD=your_password
# PHENOML_BASE_URL=https://api.phenoml.com
```

### Basic Usage

#### Mock System (Development/Testing)

```bash
# Interactive mode
python main_comprehensive.py --interactive --mock

# Single query
python main_comprehensive.py --query "I have chest pain and shortness of breath" --mock

# Batch processing
python main_comprehensive.py --batch sample_batch_queries.json --mock

# With patient demographics
python main_comprehensive.py --query "I need a checkup" --demographics '{"age": 30, "gender": "female"}' --mock
```

#### Real PhenoML System (Production)

```bash
# Interactive mode with real PhenoML
python main_comprehensive.py --interactive --real

# Single query with real PhenoML
python main_comprehensive.py --query "I have chest pain and shortness of breath" --real

# Batch processing with real PhenoML
python main_comprehensive.py --batch sample_batch_queries.json --real
```

## 🏗️ System Architecture

### Core Components

#### Mock System
1. **PhenoML Prompt Template** (`phenoml_prompt_template.py`)
   - Comprehensive prompt engineering for healthcare queries
   - Clinical guidelines integration
   - Structured JSON output formatting

2. **Mock Integration** (`phenoml_integration.py`)
   - MockPhenoMLClient for testing
   - HealthcareQueryProcessor for query handling
   - Batch processing capabilities

#### Real PhenoML System
1. **Real PhenoML Integration** (`phenoml_real_integration.py`)
   - PhenoMLRealClient using official SDK
   - HealthcareAgentManager for agent lifecycle
   - FHIR resource creation and management

2. **Agent Creation** (`build_agent.ipynb`)
   - Jupyter notebook for agent setup
   - Prompt creation and management
   - FHIR provider integration

### Shared Components
1. **JSON Schema** (`appointment_schema.json`)
   - Complete appointment booking data structure
   - Validation schema for all outputs

2. **Testing Framework** (`test_framework.py`)
   - Comprehensive test suite
   - Quality scoring system
   - Scenario-based validation

3. **Unified Interface** (`main_comprehensive.py`)
   - Single entry point for both systems
   - Interactive and batch processing modes
   - Comprehensive CLI interface

## 📊 Output Format

The system generates comprehensive JSON output including:

```json
{
  "patient_info": {
    "age_range": "18-35|36-50|51-65|65+",
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
    "severity": "emergency|urgent|semi_urgent|routine",
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
  "confidence_score": 0.0-1.0,
  "quality_score": 0.0-1.0
}
```

## 🧪 Testing

### Run All Tests

```bash
# Comprehensive test suite
python test_framework.py

# Test with mock system
python main_comprehensive.py --interactive --mock

# Test batch processing
python main_comprehensive.py --batch sample_batch_queries.json --mock
```

### Test Individual Components

```bash
# Test prompt generation
python -c "from phenoml_prompt_template import create_phenoml_prompt; print(create_phenoml_prompt('test query'))"

# Test JSON validation
python -c "import json; from jsonschema import validate; schema = json.load(open('appointment_schema.json')); print('Schema valid')"
```

## 🏥 Clinical Guidelines

The system incorporates evidence-based guidelines from:

- **American Heart Association (AHA)**: Cardiac conditions and emergency protocols
- **American College of Emergency Physicians (ACEP)**: Emergency medicine guidelines
- **American Academy of Pediatrics (AAP)**: Pediatric care standards
- **American Psychiatric Association (APA)**: Mental health assessment protocols
- **Centers for Disease Control and Prevention (CDC)**: Public health guidelines

## 🔧 Configuration

### Environment Variables

```env
# PhenoML Authentication
PHENOML_USERNAME=your_phenoml_username
PHENOML_PASSWORD=your_phenoml_password
PHENOML_BASE_URL=https://api.phenoml.com

# Optional: FHIR Server Configuration
FHIR_SERVER_URL=https://your-fhir-server.com
FHIR_API_KEY=your_fhir_api_key

# Optional: Logging Configuration
LOG_LEVEL=INFO

# Optional: Provider Configuration
HEALTHCARE_PROVIDER_ID=your_provider_id
```

### Sample Code Usage

#### Mock System
```python
from phenoml_integration import MockPhenoMLClient, HealthcareQueryProcessor

# Initialize mock system
client = MockPhenoMLClient()
processor = HealthcareQueryProcessor(client)

# Process query
result = processor.process_query(
    "I have a headache and fever",
    {"age": 30, "gender": "female"}
)
```

#### Real PhenoML System
```python
from phenoml_real_integration import HealthcareAgentManager

# Initialize real system
manager = HealthcareAgentManager()
setup_result = manager.setup_healthcare_system()

# Process query
result = manager.process_patient_query(
    "I have chest pain and shortness of breath",
    {"age": 45, "gender": "male", "medical_history": "Hypertension"}
)
```

## 📁 File Structure

```
AI_agent_hackathon/
├── README.md                          # This file
├── SYSTEM_OVERVIEW.md                 # Detailed system documentation
├── requirements.txt                   # Python dependencies
├── .env.template                      # Environment configuration template
├── appointment_schema.json            # JSON schema for validation
├── config.py                         # Configuration management
├── sample_batch_queries.json         # Sample queries for batch processing
│
├── phenoml_prompt_template.py        # Prompt engineering for healthcare
├── phenoml_integration.py            # Mock PhenoML integration
├── phenoml_real_integration.py       # Real PhenoML SDK integration
├── build_agent.ipynb                # Jupyter notebook for agent creation
│
├── example_queries.py                # Example healthcare scenarios
├── test_framework.py                 # Comprehensive testing framework
├── main.py                          # Original main script (mock only)
├── main_comprehensive.py            # Unified interface for both systems
│
└── test_report.txt                   # Latest test results
```

## 🚀 Production Deployment

### Real PhenoML Integration

1. **Setup PhenoML Account**: Obtain credentials from PhenoML
2. **Configure Environment**: Set up `.env` file with real credentials
3. **Initialize Agents**: Run the setup to create healthcare agents
4. **FHIR Integration**: Configure FHIR server connections
5. **Deploy**: Use the real system for production queries

### FHIR Server Integration

The real PhenoML system integrates directly with FHIR servers for:
- Patient record management
- Appointment scheduling
- Clinical data storage
- Medication tracking
- Condition documentation

## 🔒 Security and Compliance

- **Data Protection**: No PHI stored permanently
- **Secure Authentication**: Token-based API authentication
- **Input Validation**: Comprehensive input sanitization
- **Error Handling**: Secure error handling without data exposure
- **HIPAA Considerations**: Designed with healthcare privacy in mind

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Add tests for new functionality
4. Ensure all tests pass (`python test_framework.py`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
- Open a GitHub issue
- Check the [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) for detailed documentation
- Review the example queries in `example_queries.py`
- Test with the mock system first before using real PhenoML integration

## 🔮 Future Enhancements

- **Multi-language Support**: Support for non-English healthcare queries
- **Advanced Analytics**: Detailed analytics and reporting capabilities
- **Provider Integration**: Direct integration with healthcare provider systems
- **Real-time Guidelines**: Dynamic updates from medical guideline databases
- **Mobile App Integration**: REST API for mobile applications