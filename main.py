"""
Main Application for PhenoML Healthcare Query Processing
This is the main entry point for the healthcare appointment booking system.
"""

import json
import argparse
import logging
from typing import Dict, Any, Optional

from phenoml_integration import PhenoMLClient, HealthcareQueryProcessor, MockPhenoMLClient
from example_queries import EXAMPLE_QUERIES, get_example_by_scenario
from test_framework import HealthcareScenarioTester

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HealthcareAppointmentSystem:
    """
    Main healthcare appointment booking system.
    """
    
    def __init__(self, use_mock: bool = False, phenoml_base_url: str = None, auth_token: str = None):
        """
        Initialize the healthcare appointment system.
        
        Args:
            use_mock (bool): Whether to use mock client for testing
            phenoml_base_url (str): Base URL for PhenoML API
            auth_token (str): Authentication token for PhenoML
        """
        if use_mock:
            self.client = MockPhenoMLClient()
            logger.info("Using mock PhenoML client for testing")
        else:
            self.client = PhenoMLClient(
                base_url=phenoml_base_url or "https://experiment.app.pheno.ml",
                auth_token=auth_token
            )
            logger.info("Using real PhenoML client")
        
        self.processor = HealthcareQueryProcessor(self.client)
    
    def process_single_query(self, query: str, patient_demographics: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a single healthcare query.
        
        Args:
            query (str): Patient's healthcare query
            patient_demographics (Dict[str, Any]): Optional patient demographics
            
        Returns:
            Dict[str, Any]: Processed appointment booking data
        """
        logger.info(f"Processing query: {query[:50]}...")
        
        result = self.processor.process_query(query, patient_demographics)
        
        if result["success"]:
            logger.info(f"Query processed successfully with quality score: {result.get('quality_score', 'N/A')}")
        else:
            logger.error("Query processing failed")
        
        return result
    
    def process_batch_queries(self, queries: list) -> list:
        """
        Process multiple queries in batch.
        
        Args:
            queries (list): List of query dictionaries
            
        Returns:
            list: List of processed results
        """
        logger.info(f"Processing {len(queries)} queries in batch...")
        
        results = []
        for i, query_data in enumerate(queries):
            logger.info(f"Processing query {i+1}/{len(queries)}")
            
            if isinstance(query_data, str):
                query_data = {"query": query_data}
            
            result = self.process_single_query(
                query_data["query"],
                query_data.get("demographics")
            )
            results.append(result)
        
        success_count = sum(1 for r in results if r["success"])
        logger.info(f"Batch processing completed: {success_count}/{len(queries)} successful")
        
        return results
    
    def run_example_scenarios(self, scenario_type: str = None) -> Dict[str, Any]:
        """
        Run example scenarios for demonstration.
        
        Args:
            scenario_type (str): Type of scenario to run (emergency, routine, etc.)
            
        Returns:
            Dict[str, Any]: Results from scenario testing
        """
        if scenario_type:
            examples = get_example_by_scenario(scenario_type)
            logger.info(f"Running {len(examples)} {scenario_type} scenarios")
        else:
            examples = EXAMPLE_QUERIES
            logger.info(f"Running all {len(examples)} example scenarios")
        
        tester = HealthcareScenarioTester(self.client)
        results = tester.run_scenario_tests(examples)
        
        return results
    
    def interactive_mode(self):
        """
        Run the system in interactive mode for testing.
        """
        print("\n" + "="*60)
        print("HEALTHCARE APPOINTMENT BOOKING SYSTEM - INTERACTIVE MODE")
        print("="*60)
        print("Enter healthcare queries to get structured appointment booking data.")
        print("Type 'quit' to exit, 'examples' to see example scenarios.")
        print("Type 'help' for more commands.")
        print()
        
        while True:
            try:
                user_input = input("Enter your healthcare query: ").strip()
                
                if user_input.lower() == 'quit':
                    print("Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                elif user_input.lower() == 'examples':
                    self._show_examples()
                    continue
                elif user_input.lower().startswith('test '):
                    scenario_type = user_input[5:].strip()
                    self._run_test_scenario(scenario_type)
                    continue
                elif not user_input:
                    print("Please enter a query or command.")
                    continue
                
                # Process the query
                result = self.process_single_query(user_input)
                
                # Display results
                self._display_result(result)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"An error occurred: {e}")
    
    def _show_help(self):
        """Show help information."""
        print("\nAvailable commands:")
        print("- quit: Exit the program")
        print("- help: Show this help message")
        print("- examples: Show example queries")
        print("- test <scenario>: Run test scenarios (emergency, routine, chronic, mental_health, pediatric)")
        print("- Or enter any healthcare query to process it")
        print()
    
    def _show_examples(self):
        """Show example queries."""
        print("\nExample healthcare queries:")
        for i, example in enumerate(EXAMPLE_QUERIES[:3], 1):
            print(f"{i}. {example['query']}")
        print("...")
        print(f"Total examples available: {len(EXAMPLE_QUERIES)}")
        print()
    
    def _run_test_scenario(self, scenario_type: str):
        """Run a specific test scenario."""
        print(f"\nRunning {scenario_type} test scenarios...")
        results = self.run_example_scenarios(scenario_type)
        
        print(f"Test Results: {results['passed']}/{results['total_tests']} passed")
        print(f"Success Rate: {results['success_rate']:.2%}")
        
        if results['errors']:
            print("Errors encountered:")
            for error in results['errors']:
                print(f"- {error}")
        print()
    
    def _display_result(self, result: Dict[str, Any]):
        """Display processing result in a formatted way."""
        print("\n" + "-"*50)
        print("PROCESSING RESULT")
        print("-"*50)
        
        if not result["success"]:
            print("❌ Processing failed")
            return
        
        appointment_data = result["appointment_data"]
        
        print("✅ Processing successful")
        print(f"Quality Score: {result.get('quality_score', 'N/A'):.2f}")
        print()
        
        # Key information
        print("📋 APPOINTMENT SUMMARY:")
        print(f"Priority: {appointment_data.get('priority_level', 'N/A').upper()}")
        
        appointment_req = appointment_data.get('appointment_request', {})
        print(f"Type: {appointment_req.get('appointment_type', 'N/A')}")
        print(f"Urgency: {appointment_req.get('urgency', 'N/A')}")
        
        if appointment_req.get('specialty_required', 'none') != 'none':
            print(f"Specialty: {appointment_req.get('specialty_required')}")
        
        # Symptoms
        symptoms = appointment_data.get('symptoms_assessment', {})
        if symptoms.get('primary_symptoms'):
            print(f"\n🩺 PRIMARY SYMPTOMS:")
            for symptom in symptoms['primary_symptoms'][:3]:  # Show first 3
                print(f"- {symptom.get('symptom', 'N/A')} ({symptom.get('severity', 'N/A')})")
        
        # Guidelines
        guidelines = appointment_data.get('clinical_guidelines', {})
        if guidelines.get('applicable_guidelines'):
            print(f"\n📚 CLINICAL GUIDELINES:")
            for guideline in guidelines['applicable_guidelines'][:2]:  # Show first 2
                print(f"- {guideline.get('guideline_name', 'N/A')}")
        
        print("\n" + "="*50)
        print()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Healthcare Appointment Booking System")
    parser.add_argument("--mock", action="store_true", help="Use mock client for testing")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--query", type=str, help="Process a single query")
    parser.add_argument("--examples", action="store_true", help="Run example scenarios")
    parser.add_argument("--scenario", type=str, help="Run specific scenario type")
    parser.add_argument("--batch", type=str, help="Process queries from JSON file")
    parser.add_argument("--output", type=str, help="Output file for results")
    
    args = parser.parse_args()
    
    # Initialize system
    system = HealthcareAppointmentSystem(use_mock=args.mock)
    
    try:
        if args.interactive:
            system.interactive_mode()
        elif args.query:
            result = system.process_single_query(args.query)
            output = json.dumps(result, indent=2)
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output)
                print(f"Result saved to {args.output}")
            else:
                print(output)
        elif args.examples:
            results = system.run_example_scenarios(args.scenario)
            
            tester = HealthcareScenarioTester(system.client)
            report = tester.generate_test_report(results)
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(report)
                print(f"Test report saved to {args.output}")
            else:
                print(report)
        elif args.batch:
            with open(args.batch, 'r') as f:
                queries = json.load(f)
            
            results = system.process_batch_queries(queries)
            output = json.dumps(results, indent=2)
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output)
                print(f"Batch results saved to {args.output}")
            else:
                print(output)
        else:
            # Default: run interactive mode
            system.interactive_mode()
            
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()