#!/usr/bin/env python3
"""
Comprehensive Healthcare Query Processing System

This script provides a unified interface for healthcare query processing
using either the mock system or the real PhenoML SDK integration.
"""

import argparse
import json
import logging
import sys
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)
logger = logging.getLogger(__name__)

def setup_mock_system():
    """Set up the mock healthcare system."""
    try:
        from phenoml_integration import MockPhenoMLClient, HealthcareQueryProcessor
        
        client = MockPhenoMLClient()
        processor = HealthcareQueryProcessor(client)
        
        logger.info("Mock healthcare system initialized")
        return processor, "mock"
        
    except ImportError as e:
        logger.error(f"Failed to import mock system: {e}")
        return None, None

def setup_real_system():
    """Set up the real PhenoML healthcare system."""
    try:
        from phenoml_real_integration import HealthcareAgentManager
        
        manager = HealthcareAgentManager()
        setup_result = manager.setup_healthcare_system()
        
        logger.info(f"Real PhenoML system initialized: {setup_result}")
        return manager, "real"
        
    except ImportError as e:
        logger.error(f"PhenoML SDK not available: {e}")
        logger.info("Install with: pip install phenoml")
        return None, None
    except Exception as e:
        logger.error(f"Failed to setup real PhenoML system: {e}")
        return None, None

def process_single_query(processor, system_type: str, query: str, patient_demographics: Optional[Dict[str, Any]] = None):
    """Process a single healthcare query."""
    try:
        if system_type == "mock":
            result = processor.process_query(query, patient_demographics)
        else:  # real system
            result = processor.process_patient_query(query, patient_demographics)
        
        if result and result.get("success", True):
            quality_score = result.get("quality_score", 0.0)
            logger.info(f"Query processed successfully with quality score: {quality_score}")
            
            # Print formatted result
            print(json.dumps(result, indent=2, default=str))
            return True
        else:
            logger.error("Query processing failed")
            print(json.dumps(result, indent=2, default=str))
            return False
            
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return False

def process_batch_queries(processor, system_type: str, batch_file: str):
    """Process multiple queries from a JSON file."""
    try:
        with open(batch_file, 'r') as f:
            batch_data = json.load(f)
        
        queries = batch_data.get("queries", [])
        logger.info(f"Processing {len(queries)} queries in batch...")
        
        results = []
        successful = 0
        
        for i, query_data in enumerate(queries, 1):
            logger.info(f"Processing query {i}/{len(queries)}")
            
            query = query_data.get("query", "")
            patient_demographics = query_data.get("patient_demographics")
            
            logger.info(f"Processing query: {query[:50]}...")
            
            if system_type == "mock":
                result = processor.process_query(query, patient_demographics)
            else:  # real system
                result = processor.process_patient_query(query, patient_demographics)
            
            if result and result.get("success", True):
                successful += 1
                quality_score = result.get("quality_score", 0.0)
                logger.info(f"Query processed successfully with quality score: {quality_score}")
            else:
                logger.error("Query processing failed")
            
            results.append(result)
        
        logger.info(f"Batch processing completed: {successful}/{len(queries)} successful")
        
        # Print results
        print(json.dumps(results, indent=2, default=str))
        return successful == len(queries)
        
    except FileNotFoundError:
        logger.error(f"Batch file not found: {batch_file}")
        return False
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in batch file: {batch_file}")
        return False
    except Exception as e:
        logger.error(f"Error processing batch queries: {e}")
        return False

def run_interactive_mode(processor, system_type: str):
    """Run in interactive mode for continuous query processing."""
    print(f"\n🏥 Healthcare Query Processing System ({system_type} mode)")
    print("=" * 60)
    print("Enter healthcare queries to process them into appointment booking data.")
    print("Type 'quit' or 'exit' to stop, 'help' for commands.\n")
    
    while True:
        try:
            query = input("Healthcare Query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            elif query.lower() == 'help':
                print("\nCommands:")
                print("  help - Show this help message")
                print("  quit/exit/q - Exit the program")
                print("  Any other text - Process as healthcare query\n")
                continue
            elif not query:
                continue
            
            print(f"\nProcessing: {query}")
            print("-" * 40)
            
            success = process_single_query(processor, system_type, query)
            
            if success:
                print("✅ Query processed successfully\n")
            else:
                print("❌ Query processing failed\n")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error in interactive mode: {e}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Healthcare Query Processing System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode with mock system
  python main_comprehensive.py --interactive --mock
  
  # Process single query with real PhenoML
  python main_comprehensive.py --query "I have chest pain" --real
  
  # Process batch queries with mock system
  python main_comprehensive.py --batch sample_batch_queries.json --mock
  
  # Process query with patient demographics
  python main_comprehensive.py --query "I need a checkup" --demographics '{"age": 30, "gender": "female"}' --mock
        """
    )
    
    # System selection
    system_group = parser.add_mutually_exclusive_group(required=True)
    system_group.add_argument("--mock", action="store_true", help="Use mock PhenoML system")
    system_group.add_argument("--real", action="store_true", help="Use real PhenoML SDK")
    
    # Processing modes
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--query", type=str, help="Single healthcare query to process")
    mode_group.add_argument("--batch", type=str, help="JSON file with batch queries")
    mode_group.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    # Optional parameters
    parser.add_argument("--demographics", type=str, help="Patient demographics as JSON string")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Set logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # Parse demographics if provided
    patient_demographics = None
    if args.demographics:
        try:
            patient_demographics = json.loads(args.demographics)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in demographics parameter")
            return 1
    
    # Initialize system
    if args.mock:
        processor, system_type = setup_mock_system()
        if not processor:
            logger.error("Failed to initialize mock system")
            return 1
    else:  # args.real
        processor, system_type = setup_real_system()
        if not processor:
            logger.error("Failed to initialize real PhenoML system")
            return 1
    
    # Process based on mode
    try:
        if args.interactive:
            run_interactive_mode(processor, system_type)
            return 0
        elif args.query:
            success = process_single_query(processor, system_type, args.query, patient_demographics)
            return 0 if success else 1
        elif args.batch:
            success = process_batch_queries(processor, system_type, args.batch)
            return 0 if success else 1
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())