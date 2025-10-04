"""
Configuration settings for the PhenoML Healthcare Query Processing System.
"""

import os
from typing import Dict, Any

# PhenoML API Configuration
PHENOML_CONFIG = {
    "base_url": os.getenv("PHENOML_BASE_URL", "https://experiment.app.pheno.ml"),
    "auth_token": os.getenv("PHENOML_AUTH_TOKEN", "WW91Z09FTDN5dzljc1lIdkFFMF80UTpRM1lQVFZPanloeU1KZWY4T2ZndW9n"),
    "timeout": int(os.getenv("PHENOML_TIMEOUT", "30")),
    "max_retries": int(os.getenv("PHENOML_MAX_RETRIES", "3"))
}

# Processing Configuration
PROCESSING_CONFIG = {
    "temperature": float(os.getenv("AI_TEMPERATURE", "0.1")),  # Low for consistent medical responses
    "max_tokens": int(os.getenv("AI_MAX_TOKENS", "2000")),
    "confidence_threshold": float(os.getenv("CONFIDENCE_THRESHOLD", "0.7")),
    "use_simple_prompt": os.getenv("USE_SIMPLE_PROMPT", "false").lower() == "true"
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": os.getenv("LOG_FILE", None)  # None means log to console
}

# Safety Configuration
SAFETY_CONFIG = {
    "emergency_keywords": [
        "chest pain", "difficulty breathing", "severe bleeding", "unconscious",
        "stroke", "heart attack", "severe allergic reaction", "poisoning",
        "severe trauma", "suicidal", "overdose"
    ],
    "red_flag_symptoms": [
        "sudden severe headache", "chest pain with radiation", "severe shortness of breath",
        "loss of consciousness", "severe abdominal pain", "signs of stroke",
        "severe allergic reaction", "difficulty swallowing", "severe bleeding"
    ],
    "always_emergency_age_ranges": ["0-1"],  # Infants always need urgent evaluation
    "high_risk_combinations": [
        ["chest pain", "shortness of breath"],
        ["headache", "fever", "neck stiffness"],
        ["abdominal pain", "vomiting", "fever"]
    ]
}

# Clinical Guidelines Configuration
GUIDELINES_CONFIG = {
    "primary_sources": [
        "WHO", "CDC", "AHA", "ACP", "AAP", "ACOG", "APA", "NICE", "ESC"
    ],
    "specialty_guidelines": {
        "cardiology": ["AHA/ACC Guidelines", "ESC Guidelines"],
        "neurology": ["AAN Guidelines", "International Headache Society"],
        "pediatrics": ["AAP Guidelines", "CDC Pediatric Guidelines"],
        "psychiatry": ["APA Guidelines", "NICE Mental Health Guidelines"],
        "emergency": ["ACEP Guidelines", "ECC Guidelines"]
    }
}

# Appointment Routing Configuration
ROUTING_CONFIG = {
    "emergency_conditions": [
        "acute coronary syndrome", "stroke", "severe trauma", "anaphylaxis",
        "severe respiratory distress", "altered mental status"
    ],
    "urgent_care_conditions": [
        "minor injuries", "acute infections", "moderate pain", "fever in adults",
        "urinary tract infections", "minor burns"
    ],
    "primary_care_conditions": [
        "routine check-ups", "chronic disease management", "preventive care",
        "mild acute illnesses", "medication refills"
    ],
    "specialist_referrals": {
        "cardiology": ["chest pain", "heart palpitations", "hypertension"],
        "neurology": ["headaches", "seizures", "memory problems"],
        "orthopedics": ["joint pain", "fractures", "sports injuries"],
        "dermatology": ["skin conditions", "rashes", "moles"],
        "psychiatry": ["depression", "anxiety", "bipolar disorder"]
    }
}

# Testing Configuration
TESTING_CONFIG = {
    "mock_mode": os.getenv("MOCK_MODE", "false").lower() == "true",
    "test_scenarios_file": "example_queries.py",
    "test_report_file": "test_report.txt",
    "performance_threshold": float(os.getenv("PERFORMANCE_THRESHOLD", "0.8"))
}

# Output Configuration
OUTPUT_CONFIG = {
    "include_confidence_scores": True,
    "include_processing_metadata": True,
    "pretty_print_json": True,
    "validate_output": True,
    "save_processing_logs": os.getenv("SAVE_LOGS", "false").lower() == "true"
}

def get_config(section: str = None) -> Dict[str, Any]:
    """
    Get configuration for a specific section or all configuration.
    
    Args:
        section (str): Configuration section name
        
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    all_config = {
        "phenoml": PHENOML_CONFIG,
        "processing": PROCESSING_CONFIG,
        "logging": LOGGING_CONFIG,
        "safety": SAFETY_CONFIG,
        "guidelines": GUIDELINES_CONFIG,
        "routing": ROUTING_CONFIG,
        "testing": TESTING_CONFIG,
        "output": OUTPUT_CONFIG
    }
    
    if section:
        return all_config.get(section, {})
    
    return all_config

def validate_config() -> bool:
    """
    Validate configuration settings.
    
    Returns:
        bool: True if configuration is valid
    """
    # Check required environment variables
    required_vars = ["PHENOML_BASE_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: Missing environment variables: {missing_vars}")
        print("Using default values...")
    
    # Validate numeric ranges
    if not (0.0 <= PROCESSING_CONFIG["temperature"] <= 2.0):
        print("Warning: AI temperature should be between 0.0 and 2.0")
        return False
    
    if not (0.0 <= PROCESSING_CONFIG["confidence_threshold"] <= 1.0):
        print("Warning: Confidence threshold should be between 0.0 and 1.0")
        return False
    
    return True

# Environment-specific configurations
ENVIRONMENT_CONFIGS = {
    "development": {
        "phenoml": {**PHENOML_CONFIG, "timeout": 60},
        "logging": {**LOGGING_CONFIG, "level": "DEBUG"},
        "testing": {**TESTING_CONFIG, "mock_mode": True}
    },
    "production": {
        "phenoml": {**PHENOML_CONFIG, "timeout": 30},
        "logging": {**LOGGING_CONFIG, "level": "INFO"},
        "testing": {**TESTING_CONFIG, "mock_mode": False}
    },
    "testing": {
        "phenoml": {**PHENOML_CONFIG, "timeout": 10},
        "logging": {**LOGGING_CONFIG, "level": "WARNING"},
        "testing": {**TESTING_CONFIG, "mock_mode": True}
    }
}

def get_environment_config(environment: str = None) -> Dict[str, Any]:
    """
    Get configuration for a specific environment.
    
    Args:
        environment (str): Environment name (development, production, testing)
        
    Returns:
        Dict[str, Any]: Environment-specific configuration
    """
    env = environment or os.getenv("ENVIRONMENT", "development")
    return ENVIRONMENT_CONFIGS.get(env, ENVIRONMENT_CONFIGS["development"])

if __name__ == "__main__":
    # Validate configuration when run directly
    if validate_config():
        print("Configuration validation passed")
        print(f"Current environment: {os.getenv('ENVIRONMENT', 'development')}")
    else:
        print("Configuration validation failed")