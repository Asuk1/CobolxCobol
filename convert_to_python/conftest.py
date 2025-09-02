"""
conftest.py - Shared pytest configuration and fixtures
This file contains common setup, fixtures, and utilities shared across all test modules.
Pytest automatically discovers and loads this file.
"""

import pytest
import io
import sys
from unittest.mock import patch, MagicMock
from accountsystem import AccountSystem


@pytest.fixture
def account_system():
    """
    Fixture providing a fresh AccountSystem instance for each test.
    Ensures initial balance is 1000.00 as expected by all tests.
    """
    acc = AccountSystem()
    assert acc.balance == 1000.00  # Validate setup
    return acc


@pytest.fixture
def fresh_account():
    """
    Alternative fixture name for AccountSystem instance.
    Provides the same functionality as account_system fixture.
    """
    return AccountSystem()


# Shared constants that might be used across multiple test files
INITIAL_BALANCE = 1000.00
EXPECTED_MESSAGES = {
    'credit': 'Amount credited',
    'debit': 'Amount debited',
    'insufficient': 'Insufficient funds',
    'invalid_amount': 'Invalid amount',
    'invalid_input': 'Invalid input',
    'current_balance': 'Current balance:',
    'system_title': 'Account Management System',
    'exit_message': 'Exiting the program. Goodbye!',
    'invalid_choice': 'Invalid choice'
}


def run_all_tests():
    """
    Utility function to run all test files in the test suite.
    This replaces the original run_comprehensive_tests function.
    """
    print("=== EXECUTING PYTHON TEST SUITE ===")
    print("Equivalent to running test_account.cob in COBOL")
    print("Running all test modules...")
    print()
    
    # Run all test files with pytest
    result = pytest.main([
        "-v",                    # Verbose mode
        "--tb=short",            # Short traceback
        "-x",                    # Stop on first failure
        "test_account_basic.py",
        "test_account_validation.py", 
        "test_account_integration.py",
        "test_account_edge_cases.py"
    ])
    
    print()
    print("=== TEST EXECUTION COMPLETE ===")
    return result


if __name__ == "__main__":
    run_all_tests() 