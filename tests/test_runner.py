"""
test_runner.py - Centralized test runner for the complete AccountSystem test suite

This script provides a convenient way to run all test modules together,
maintaining compatibility with the original run_comprehensive_tests() function.
It can be used as a replacement for the original monolithic test file execution.

Usage:
    python test_runner.py              # Run all tests
    python test_runner.py --basic      # Run only basic tests
    python test_runner.py --validation # Run only validation tests
    python test_runner.py --integration # Run only integration tests
    python test_runner.py --edge       # Run only edge case tests
"""

import pytest
import sys
import argparse


def run_comprehensive_tests(test_modules=None):
    """
    Execute all tests and display complete report.
    Equivalent to running test_account.cob in COBOL.
    
    Args:
        test_modules: List of specific test modules to run, or None for all tests
    """
    print("=== EXECUTING PYTHON TEST SUITE ===")
    print("Equivalent to running test_account.cob in COBOL")
    print("Refactored into modular test files for better organization")
    
    if test_modules:
        print(f"Running specific modules: {', '.join(test_modules)}")
    else:
        print("Running all test modules...")
    print()
    
    # Default test files if none specified
    if not test_modules:
        test_modules = [
            "test_account_basic.py",
            "test_account_validation.py", 
            "test_account_integration.py",
            "test_account_edge_cases.py"
        ]
    
    # Run tests with pytest
    pytest_args = [
        "-v",                    # Verbose mode
        "--tb=short",            # Short traceback
        "-x",                    # Stop on first failure
    ]
    pytest_args.extend(test_modules)
    
    result = pytest.main(pytest_args)
    
    print()
    print("=== TEST EXECUTION COMPLETE ===")
    
    if result == 0:
        print("✓ All tests passed successfully!")
    else:
        print("✗ Some tests failed. See output above for details.")
    
    return result


def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(
        description="Run AccountSystem test suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_runner.py                    # Run all tests
  python test_runner.py --basic            # Run only basic functionality tests
  python test_runner.py --validation       # Run only input validation tests
  python test_runner.py --integration      # Run only integration tests  
  python test_runner.py --edge             # Run only edge case tests
  python test_runner.py --basic --validation # Run basic and validation tests
        """
    )
    
    parser.add_argument('--basic', action='store_true',
                       help='Run basic functionality tests')
    parser.add_argument('--validation', action='store_true', 
                       help='Run input validation tests')
    parser.add_argument('--integration', action='store_true',
                       help='Run integration and menu tests')
    parser.add_argument('--edge', action='store_true',
                       help='Run edge case and boundary tests')
    
    args = parser.parse_args()
    
    # Determine which test modules to run based on arguments
    test_modules = []
    
    if args.basic:
        test_modules.append("test_account_basic.py")
    if args.validation:
        test_modules.append("test_account_validation.py")
    if args.integration:
        test_modules.append("test_account_integration.py")
    if args.edge:
        test_modules.append("test_account_edge_cases.py")
    
    # If no specific modules selected, run all tests
    if not test_modules:
        test_modules = None
    
    # Execute tests
    result = run_comprehensive_tests(test_modules)
    
    # Exit with appropriate code
    sys.exit(result)


if __name__ == "__main__":
    main()