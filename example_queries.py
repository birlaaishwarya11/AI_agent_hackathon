"""
Example Healthcare Queries and Expected JSON Outputs
This module contains sample queries and their corresponding structured outputs
for testing and demonstration purposes.
"""

EXAMPLE_QUERIES = [
    {
        "query": "I'm a 28-year-old male and I've been having severe chest pain for the last 3 hours. It feels like someone is squeezing my chest and the pain radiates to my left arm. I'm also feeling nauseous and sweaty.",
        "expected_output": {
            "patient_info": {
                "age_range": "18-35",
                "gender": "male",
                "pregnancy_status": "not_applicable",
                "chronic_conditions": []
            },
            "symptoms_assessment": {
                "primary_symptoms": [
                    {
                        "symptom": "severe chest pain with radiation to left arm",
                        "body_system": "cardiovascular",
                        "severity": "severe"
                    },
                    {
                        "symptom": "nausea",
                        "body_system": "gastrointestinal",
                        "severity": "moderate"
                    },
                    {
                        "symptom": "diaphoresis",
                        "body_system": "general",
                        "severity": "moderate"
                    }
                ],
                "severity": "emergency",
                "duration": "acute",
                "onset": "sudden",
                "red_flags": [
                    "chest pain with arm radiation",
                    "associated nausea and diaphoresis",
                    "possible acute coronary syndrome"
                ]
            },
            "appointment_request": {
                "appointment_type": "emergency",
                "specialty_required": "cardiology",
                "urgency": "immediate",
                "preferred_timeframe": "immediate",
                "appointment_reason": "Acute chest pain with cardiac risk features"
            },
            "clinical_guidelines": {
                "applicable_guidelines": [
                    {
                        "guideline_name": "AHA/ACC Guidelines for Management of Acute Coronary Syndromes",
                        "organization": "American Heart Association",
                        "relevance": "primary"
                    },
                    {
                        "guideline_name": "ESC Guidelines for Acute Coronary Syndromes",
                        "organization": "European Society of Cardiology",
                        "relevance": "primary"
                    }
                ],
                "recommendations": [
                    "Immediate ECG and cardiac biomarkers",
                    "Emergency department evaluation",
                    "Consider acute coronary syndrome protocol"
                ],
                "contraindications": [
                    "Do not delay emergency care",
                    "Avoid discharge without cardiac evaluation"
                ]
            },
            "priority_level": "emergency",
            "additional_notes": {
                "patient_concerns": "Severe chest pain with concerning features",
                "follow_up_needed": True,
                "diagnostic_tests_suggested": [
                    "ECG",
                    "Troponin levels",
                    "Chest X-ray",
                    "Complete blood count"
                ],
                "lifestyle_factors": []
            },
            "confidence_score": 0.95
        }
    },
    {
        "query": "Hi, I'm a 35-year-old woman and I've been having a persistent cough for about 2 weeks now. It's mostly dry but sometimes I cough up a little clear mucus. I don't have a fever but I feel tired. I work in an office environment.",
        "expected_output": {
            "patient_info": {
                "age_range": "18-35",
                "gender": "female",
                "pregnancy_status": "unknown",
                "chronic_conditions": []
            },
            "symptoms_assessment": {
                "primary_symptoms": [
                    {
                        "symptom": "persistent dry cough with minimal clear sputum",
                        "body_system": "respiratory",
                        "severity": "mild"
                    },
                    {
                        "symptom": "fatigue",
                        "body_system": "general",
                        "severity": "mild"
                    }
                ],
                "severity": "low",
                "duration": "subacute",
                "onset": "gradual",
                "red_flags": []
            },
            "appointment_request": {
                "appointment_type": "primary_care",
                "specialty_required": "none",
                "urgency": "within_week",
                "preferred_timeframe": "within a week",
                "appointment_reason": "Persistent cough evaluation"
            },
            "clinical_guidelines": {
                "applicable_guidelines": [
                    {
                        "guideline_name": "ACCP Guidelines for Diagnosis and Management of Cough",
                        "organization": "American College of Chest Physicians",
                        "relevance": "primary"
                    },
                    {
                        "guideline_name": "NICE Guidelines for Respiratory Tract Infections",
                        "organization": "National Institute for Health and Care Excellence",
                        "relevance": "secondary"
                    }
                ],
                "recommendations": [
                    "Clinical evaluation for post-infectious cough",
                    "Consider chest examination and history",
                    "Assess for underlying respiratory conditions"
                ],
                "contraindications": [
                    "Monitor for worsening symptoms",
                    "Return if fever develops or cough worsens"
                ]
            },
            "priority_level": "routine",
            "additional_notes": {
                "patient_concerns": "Persistent cough affecting daily activities",
                "follow_up_needed": True,
                "diagnostic_tests_suggested": [
                    "Chest X-ray if symptoms persist",
                    "Peak flow measurement"
                ],
                "lifestyle_factors": [
                    "Office work environment",
                    "No smoking history mentioned"
                ]
            },
            "confidence_score": 0.85
        }
    },
    {
        "query": "I'm 67 years old, female, and I've been having increasing shortness of breath over the past month, especially when climbing stairs. I also notice my ankles are swollen by the end of the day. I have a history of high blood pressure.",
        "expected_output": {
            "patient_info": {
                "age_range": "65+",
                "gender": "female",
                "pregnancy_status": "not_applicable",
                "chronic_conditions": ["hypertension"]
            },
            "symptoms_assessment": {
                "primary_symptoms": [
                    {
                        "symptom": "exertional dyspnea",
                        "body_system": "cardiovascular",
                        "severity": "moderate"
                    },
                    {
                        "symptom": "bilateral ankle edema",
                        "body_system": "cardiovascular",
                        "severity": "moderate"
                    }
                ],
                "severity": "moderate",
                "duration": "chronic",
                "onset": "gradual",
                "red_flags": [
                    "Progressive dyspnea in elderly patient",
                    "Bilateral edema with known hypertension"
                ]
            },
            "appointment_request": {
                "appointment_type": "primary_care",
                "specialty_required": "cardiology",
                "urgency": "within_week",
                "preferred_timeframe": "within a week",
                "appointment_reason": "Evaluation of heart failure symptoms"
            },
            "clinical_guidelines": {
                "applicable_guidelines": [
                    {
                        "guideline_name": "AHA/ACC/HFSA Guidelines for Heart Failure Management",
                        "organization": "American Heart Association",
                        "relevance": "primary"
                    },
                    {
                        "guideline_name": "ESC Guidelines for Heart Failure",
                        "organization": "European Society of Cardiology",
                        "relevance": "primary"
                    }
                ],
                "recommendations": [
                    "Echocardiogram to assess cardiac function",
                    "BNP or NT-proBNP testing",
                    "Comprehensive cardiovascular evaluation"
                ],
                "contraindications": [
                    "Monitor for worsening symptoms",
                    "Seek immediate care if severe dyspnea develops"
                ]
            },
            "priority_level": "semi_urgent",
            "additional_notes": {
                "patient_concerns": "Progressive shortness of breath affecting mobility",
                "follow_up_needed": True,
                "diagnostic_tests_suggested": [
                    "Echocardiogram",
                    "BNP/NT-proBNP",
                    "Chest X-ray",
                    "Complete metabolic panel",
                    "ECG"
                ],
                "lifestyle_factors": [
                    "History of hypertension",
                    "Age-related cardiovascular risk"
                ]
            },
            "confidence_score": 0.90
        }
    },
    {
        "query": "I'm a 22-year-old college student and I've been feeling really anxious and stressed lately. I have trouble sleeping, my heart races sometimes, and I can't concentrate on my studies. This has been going on for about 3 weeks since midterm exams started.",
        "expected_output": {
            "patient_info": {
                "age_range": "18-35",
                "gender": "not_specified",
                "pregnancy_status": "unknown",
                "chronic_conditions": []
            },
            "symptoms_assessment": {
                "primary_symptoms": [
                    {
                        "symptom": "anxiety and stress",
                        "body_system": "psychiatric",
                        "severity": "moderate"
                    },
                    {
                        "symptom": "insomnia",
                        "body_system": "neurological",
                        "severity": "moderate"
                    },
                    {
                        "symptom": "palpitations",
                        "body_system": "cardiovascular",
                        "severity": "mild"
                    },
                    {
                        "symptom": "concentration difficulties",
                        "body_system": "neurological",
                        "severity": "moderate"
                    }
                ],
                "severity": "moderate",
                "duration": "subacute",
                "onset": "gradual",
                "red_flags": []
            },
            "appointment_request": {
                "appointment_type": "mental_health",
                "specialty_required": "psychiatry",
                "urgency": "within_week",
                "preferred_timeframe": "within a week",
                "appointment_reason": "Anxiety and stress management evaluation"
            },
            "clinical_guidelines": {
                "applicable_guidelines": [
                    {
                        "guideline_name": "APA Guidelines for Treatment of Anxiety Disorders",
                        "organization": "American Psychiatric Association",
                        "relevance": "primary"
                    },
                    {
                        "guideline_name": "NICE Guidelines for Anxiety Disorders",
                        "organization": "National Institute for Health and Care Excellence",
                        "relevance": "primary"
                    }
                ],
                "recommendations": [
                    "Mental health screening and assessment",
                    "Consider cognitive behavioral therapy",
                    "Evaluate for anxiety disorders"
                ],
                "contraindications": [
                    "Monitor for worsening symptoms",
                    "Assess for suicidal ideation"
                ]
            },
            "priority_level": "semi_urgent",
            "additional_notes": {
                "patient_concerns": "Academic performance affected by anxiety and sleep issues",
                "follow_up_needed": True,
                "diagnostic_tests_suggested": [
                    "Mental health screening questionnaires",
                    "Basic metabolic panel to rule out medical causes"
                ],
                "lifestyle_factors": [
                    "College student",
                    "Academic stress from midterm exams",
                    "Sleep disruption"
                ]
            },
            "confidence_score": 0.88
        }
    },
    {
        "query": "My 8-year-old daughter has had a fever of 102°F for 2 days, along with a sore throat and difficulty swallowing. She's also complaining of a headache and seems very tired. She hasn't been eating much.",
        "expected_output": {
            "patient_info": {
                "age_range": "0-17",
                "gender": "female",
                "pregnancy_status": "not_applicable",
                "chronic_conditions": []
            },
            "symptoms_assessment": {
                "primary_symptoms": [
                    {
                        "symptom": "fever 102°F",
                        "body_system": "general",
                        "severity": "moderate"
                    },
                    {
                        "symptom": "sore throat with dysphagia",
                        "body_system": "otolaryngologic",
                        "severity": "moderate"
                    },
                    {
                        "symptom": "headache",
                        "body_system": "neurological",
                        "severity": "moderate"
                    },
                    {
                        "symptom": "fatigue and decreased appetite",
                        "body_system": "general",
                        "severity": "moderate"
                    }
                ],
                "severity": "moderate",
                "duration": "acute",
                "onset": "sudden",
                "red_flags": [
                    "High fever in child",
                    "Difficulty swallowing"
                ]
            },
            "appointment_request": {
                "appointment_type": "urgent_care",
                "specialty_required": "none",
                "urgency": "within_24h",
                "preferred_timeframe": "today or tomorrow",
                "appointment_reason": "Pediatric fever and throat infection evaluation"
            },
            "clinical_guidelines": {
                "applicable_guidelines": [
                    {
                        "guideline_name": "AAP Guidelines for Fever Management in Children",
                        "organization": "American Academy of Pediatrics",
                        "relevance": "primary"
                    },
                    {
                        "guideline_name": "IDSA Guidelines for Streptococcal Pharyngitis",
                        "organization": "Infectious Diseases Society of America",
                        "relevance": "primary"
                    }
                ],
                "recommendations": [
                    "Rapid strep test and throat culture",
                    "Physical examination including throat inspection",
                    "Consider antibiotic therapy if strep positive"
                ],
                "contraindications": [
                    "Monitor for signs of dehydration",
                    "Return if fever persists or worsens",
                    "Watch for breathing difficulties"
                ]
            },
            "priority_level": "urgent",
            "additional_notes": {
                "patient_concerns": "Parent concerned about child's fever and eating difficulties",
                "follow_up_needed": True,
                "diagnostic_tests_suggested": [
                    "Rapid strep test",
                    "Throat culture",
                    "Complete blood count if indicated"
                ],
                "lifestyle_factors": [
                    "School-age child",
                    "Possible exposure to streptococcal infection"
                ]
            },
            "confidence_score": 0.92
        }
    }
]

def get_example_by_scenario(scenario_type: str):
    """
    Get example queries by scenario type.
    
    Args:
        scenario_type (str): Type of scenario (emergency, routine, pediatric, mental_health, etc.)
        
    Returns:
        list: Matching example queries
    """
    scenario_mapping = {
        "emergency": [EXAMPLE_QUERIES[0]],  # Chest pain
        "routine": [EXAMPLE_QUERIES[1]],    # Persistent cough
        "chronic": [EXAMPLE_QUERIES[2]],    # Heart failure symptoms
        "mental_health": [EXAMPLE_QUERIES[3]],  # Anxiety
        "pediatric": [EXAMPLE_QUERIES[4]]   # Child fever
    }
    
    return scenario_mapping.get(scenario_type, EXAMPLE_QUERIES)

def validate_json_output(output_json: dict) -> bool:
    """
    Validate that the JSON output contains all required fields.
    
    Args:
        output_json (dict): The JSON output to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = [
        "patient_info",
        "symptoms_assessment", 
        "appointment_request",
        "clinical_guidelines",
        "priority_level"
    ]
    
    for field in required_fields:
        if field not in output_json:
            return False
    
    return True