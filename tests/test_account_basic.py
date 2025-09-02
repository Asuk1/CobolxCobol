"""
test_account_basic.py - Basic AccountSystem functionality tests

This module contains fundamental tests that verify the core operations:
- Initial balance verification
- Balance display functionality  
- Basic credit operations (valid amounts and zero)
- Basic debit operations (valid amounts, zero, and insufficient funds)

These tests are equivalent to the basic COBOL test cases and form the foundation
of the test suite.
"""

import pytest
from unittest.mock import patch
from conftest import INITIAL_BALANCE, EXPECTED_MESSAGES


class TestAccountSystemBasic:
    """
    Basic functionality tests for AccountSystem core operations.
    These tests validate the fundamental behavior equivalent to COBOL tests.
    """
    
    def setup_method(self):
        """Setup before each test - use fresh AccountSystem instance"""
        from accountsystem import AccountSystem
        self.acc = AccountSystem()
        assert self.acc.balance == INITIAL_BALANCE  # Validate setup
    
    # Balance and display tests
    
    def test_initial_balance(self):
        """TC-1.1: Verify that initial balance is correct (1000.00)"""
        assert self.acc.balance == INITIAL_BALANCE
        
    def test_view_balance_display(self, capsys):
        """TC-1.1: Verify balance display output shows correct format"""
        self.acc.view_balance()
        captured = capsys.readouterr()
        assert f"{EXPECTED_MESSAGES['current_balance']} {INITIAL_BALANCE:.2f}" in captured.out
    
    # Basic credit operations tests
    
    @patch('builtins.input', return_value='100.00')
    def test_credit_valid_amount(self, mock_input, capsys):
        """TC-2.1: Test credit with valid amount (equivalent to COBOL Credit Valid)"""
        # Initial state
        initial_balance = self.acc.balance
        
        # Execute the actual method
        self.acc.credit_account()
        
        # Validations
        assert self.acc.balance == initial_balance + 100.00  # 1100.00
        
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['credit'] in captured.out
        assert "1100.00" in captured.out
    
    @patch('builtins.input', return_value='0.00')
    def test_credit_zero_amount(self, mock_input, capsys):
        """TC-2.2: Test credit with zero amount (equivalent to COBOL Credit Zero)"""
        initial_balance = self.acc.balance
        
        self.acc.credit_account()
        
        # Balance should remain the same
        assert self.acc.balance == initial_balance  # 1000.00
        
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['credit'] in captured.out
        assert "1000.00" in captured.out
    
    # Basic debit operations tests
    
    @patch('builtins.input', return_value='50.00')
    def test_debit_valid_amount(self, mock_input, capsys):
        """TC-3.1: Test debit with valid amount (equivalent to COBOL Debit Valid)"""
        initial_balance = self.acc.balance
        
        self.acc.debit_account()
        
        assert self.acc.balance == initial_balance - 50.00  # 950.00
        
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['debit'] in captured.out
        assert "950.00" in captured.out
    
    @patch('builtins.input', return_value='2000.00')
    def test_debit_insufficient_funds(self, mock_input, capsys):
        """TC-3.2: Test debit with insufficient funds (equivalent to COBOL Debit Insufficient)"""
        initial_balance = self.acc.balance
        
        self.acc.debit_account()
        
        # Balance should not change
        assert self.acc.balance == initial_balance  # 1000.00
        
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['insufficient'] in captured.out
    
    @patch('builtins.input', return_value='0.00')
    def test_debit_zero_amount(self, mock_input, capsys):
        """TC-3.3: Test debit with zero amount (equivalent to COBOL Debit Zero)"""
        initial_balance = self.acc.balance
        
        self.acc.debit_account()
        
        # Balance should not change
        assert self.acc.balance == initial_balance  # 1000.00
        
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['debit'] in captured.out
        assert "1000.00" in captured.out