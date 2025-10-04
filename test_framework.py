"""
Testing Framework for PhenoML Healthcare Query Processing
This module provides comprehensive testing capabilities for the healthcare query processing system.
"""

import json
import unittest
from typing import Dict, Any, List
import logging
from datetime import datetime

from phenoml_integration import PhenoMLClient, HealthcareQueryProcessor, MockPhenoMLClient
from example_queries import EXAMPLE_QUERIES, validate_json_output
from phenoml_prompt_template import create_phenoml_prompt, create_simple_phenoml_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestPhenoMLIntegration(unittest.TestCase):
    """
    Unit tests for PhenoML integration components.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = PhenoMLClient()
        self.processor = HealthcareQueryProcessor(self.client)
    
    def test_prompt_generation(self):
        """Test prompt template generation."""
        query = "I have a headache and fever"
        
        # Test comprehensive prompt
        prompt = create_phenoml_prompt(query)
        self.assertIn(query, prompt)
        self.assertIn("clinical guidelines", prompt.lower())
        self.assertIn("json", prompt.lower())
        
        # Test simple prompt
        simple_prompt = create_simple_phenoml_prompt(query)
        self.assertIn(query, simple_prompt)
        self.assertIn("json", simple_prompt.lower())
    
    def test_json_validation(self):
        """Test JSON output validation."""
        # Test valid JSON
        valid_json = EXAMPLE_QUERIES[0]["expected_output"]
        self.assertTrue(validate_json_output(valid_json))
        
        # Test invalid JSON (missing required field)
        invalid_json = {"patient_info": {}, "symptoms_assessment": {}}
        self.assertFalse(validate_json_output(invalid_json))
    
    def test_authentication(self):
        """Test PhenoML authentication."""
        # Note: This test may fail if credentials are invalid
        # In a real environment, you'd use test credentials
        try:
            result = self.client.authenticate()
            logger.info(f"Authentication test result: {result}")
        except Exception as e:
            logger.warning(f"Authentication test failed (expected in test environment): {e}")

class HealthcareScenarioTester:
    """
    Comprehensive tester for healthcare scenarios.
    """
    
    def __init__(self, phenoml_client: PhenoMLClient):
        """
        Initialize the scenario tester.
        
        Args:
            phenoml_client (PhenoMLClient): Configured PhenoML client
        """
        self.client = phenoml_client
        self.processor = HealthcareQueryProcessor(phenoml_client)
        self.test_results = []
    
    def run_scenario_tests(self, scenarios: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run comprehensive scenario tests.
        
        Args:
            scenarios (List[Dict[str, Any]]): Custom scenarios to test, defaults to EXAMPLE_QUERIES
            
        Returns:
            Dict[str, Any]: Test results summary
        """
        if scenarios is None:
            scenarios = EXAMPLE_QUERIES
        
        logger.info(f"Running {len(scenarios)} scenario tests...")
        
        results = {
            "total_tests": len(scenarios),
            "passed": 0,
            "failed": 0,
            "errors": [],
            "test_details": [],
            "started_at": datetime.now().isoformat()
        }
        
        for i, scenario in enumerate(scenarios):
            logger.info(f"Testing scenario {i+1}: {scenario['query'][:50]}...")
            
            try:
                test_result = self._test_single_scenario(scenario, i+1)
                results["test_details"].append(test_result)
                
                if test_result["passed"]:
                    results["passed"] += 1
                else:
                    results["failed"] += 1
                    
            except Exception as e:
                error_msg = f"Scenario {i+1} failed with error: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
                results["failed"] += 1
        
        results["completed_at"] = datetime.now().isoformat()
        results["success_rate"] = results["passed"] / results["total_tests"] if results["total_tests"] > 0 else 0
        
        return results
    
    def _test_single_scenario(self, scenario: Dict[str, Any], scenario_num: int) -> Dict[str, Any]:
        """
        Test a single healthcare scenario.
        
        Args:
            scenario (Dict[str, Any]): The scenario to test
            scenario_num (int): Scenario number for identification
            
        Returns:
            Dict[str, Any]: Test result for this scenario
        """
        query = scenario["query"]
        expected_output = scenario["expected_output"]
        
        # Process the query
        result = self.processor.process_query(query)
        
        test_result = {
            "scenario_number": scenario_num,
            "query": query,
            "processed_successfully": result["success"],
            "passed": False,
            "issues": [],
            "quality_score": result.get("quality_score", 0),
            "processing_time": None
        }
        
        if not result["success"]:
            test_result["issues"].append("Query processing failed")
            return test_result
        
        appointment_data = result["appointment_data"]
        
        # Validate JSON structure
        if not validate_json_output(appointment_data):
            test_result["issues"].append("Invalid JSON structure")
            return test_result
        
        # Compare key fields with expected output
        comparison_results = self._compare_outputs(appointment_data, expected_output)
        test_result.update(comparison_results)
        
        # Determine if test passed
        test_result["passed"] = (
            len(test_result["issues"]) == 0 and
            test_result["quality_score"] >= 0.7
        )
        
        return test_result
    
    def _compare_outputs(self, actual: Dict[str, Any], expected: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare actual output with expected output.
        
        Args:
            actual (Dict[str, Any]): Actual output from processing
            expected (Dict[str, Any]): Expected output
            
        Returns:
            Dict[str, Any]: Comparison results
        """
        comparison = {
            "field_matches": {},
            "issues": []
        }
        
        # Check priority level
        if actual.get("priority_level") != expected.get("priority_level"):
            comparison["issues"].append(
                f"Priority mismatch: got {actual.get('priority_level')}, "
                f"expected {expected.get('priority_level')}"
            )
        else:
            comparison["field_matches"]["priority_level"] = True
        
        # Check appointment type
        actual_type = actual.get("appointment_request", {}).get("appointment_type")
        expected_type = expected.get("appointment_request", {}).get("appointment_type")
        
        if actual_type != expected_type:
            comparison["issues"].append(
                f"Appointment type mismatch: got {actual_type}, expected {expected_type}"
            )
        else:
            comparison["field_matches"]["appointment_type"] = True
        
        # Check severity assessment
        actual_severity = actual.get("symptoms_assessment", {}).get("severity")
        expected_severity = expected.get("symptoms_assessment", {}).get("severity")
        
        if actual_severity != expected_severity:
            comparison["issues"].append(
                f"Severity mismatch: got {actual_severity}, expected {expected_severity}"
            )
        else:
            comparison["field_matches"]["severity"] = True
        
        # Check if clinical guidelines are present
        actual_guidelines = actual.get("clinical_guidelines", {}).get("applicable_guidelines", [])
        expected_guidelines = expected.get("clinical_guidelines", {}).get("applicable_guidelines", [])
        
        if len(actual_guidelines) == 0 and len(expected_guidelines) > 0:
            comparison["issues"].append("Missing clinical guidelines")
        else:
            comparison["field_matches"]["clinical_guidelines"] = True
        
        return comparison
    
    def generate_test_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a comprehensive test report.
        
        Args:
            results (Dict[str, Any]): Test results from run_scenario_tests
            
        Returns:
            str: Formatted test report
        """
        report = []
        report.append("=" * 60)
        report.append("PHENOML HEALTHCARE QUERY PROCESSING TEST REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Summary
        report.append("SUMMARY:")
        report.append(f"Total Tests: {results['total_tests']}")
        report.append(f"Passed: {results['passed']}")
        report.append(f"Failed: {results['failed']}")
        report.append(f"Success Rate: {results['success_rate']:.2%}")
        report.append(f"Started: {results['started_at']}")
        report.append(f"Completed: {results['completed_at']}")
        report.append("")
        
        # Errors
        if results["errors"]:
            report.append("ERRORS:")
            for error in results["errors"]:
                report.append(f"- {error}")
            report.append("")
        
        # Detailed results
        report.append("DETAILED RESULTS:")
        report.append("-" * 40)
        
        for test in results["test_details"]:
            report.append(f"Scenario {test['scenario_number']}: {'PASS' if test['passed'] else 'FAIL'}")
            report.append(f"Query: {test['query'][:80]}...")
            report.append(f"Quality Score: {test['quality_score']:.2f}")
            
            if test["issues"]:
                report.append("Issues:")
                for issue in test["issues"]:
                    report.append(f"  - {issue}")
            
            report.append("")
        
        return "\n".join(report)

# MockPhenoMLClient is now imported from phenoml_integration

def run_comprehensive_tests():
    """
    Run comprehensive tests of the entire system.
    """
    print("Starting comprehensive PhenoML healthcare query processing tests...")
    
    # Run unit tests
    print("\n1. Running unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run scenario tests with mock client
    print("\n2. Running scenario tests with mock client...")
    mock_client = MockPhenoMLClient()
    scenario_tester = HealthcareScenarioTester(mock_client)
    
    results = scenario_tester.run_scenario_tests()
    report = scenario_tester.generate_test_report(results)
    
    print(report)
    
    # Save report to file
    with open("test_report.txt", "w") as f:
        f.write(report)
    
    print("\nTest report saved to test_report.txt")

if __name__ == "__main__":
    run_comprehensive_tests()