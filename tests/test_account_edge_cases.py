"""
test_account_edge_cases.py - Edge cases and boundary condition tests

This module contains tests for extreme scenarios and boundary conditions:
- Minimum and maximum amounts
- Exact balance operations (debit to zero)
- Boundary values (one cent over balance)
- Extreme values that might cause overflow or precision issues

These tests ensure the system behaves correctly at the limits of its operational range
and handles unusual but valid scenarios appropriately.
"""

import pytest
from unittest.mock import patch
from conftest import INITIAL_BALANCE, EXPECTED_MESSAGES


class TestAccountSystemEdgeCases:
    """
    Edge case tests for extreme scenarios and boundary conditions.
    Tests the system's behavior at operational limits and unusual but valid inputs.
    """
    
    def setup_method(self):
        """Setup before each test - use fresh AccountSystem instance"""
        from accountsystem import AccountSystem
        self.acc = AccountSystem()
        assert self.acc.balance == INITIAL_BALANCE  # Validate setup
    
    # Minimum value boundary tests
    
    @patch('builtins.input', return_value='0.01')
    def test_credit_minimum_positive_amount(self, mock_input):
        """Test credit with smallest possible monetary amount (one cent)"""
        initial_balance = self.acc.balance
        self.acc.credit_account()
        assert self.acc.balance == initial_balance + 0.01
    
    # Maximum value boundary tests
    
    @patch('builtins.input', return_value='999999.99')
    def test_credit_maximum_amount(self, mock_input):
        """Test credit with very large amount to check for overflow handling"""
        initial_balance = self.acc.balance
        self.acc.credit_account()
        assert self.acc.balance == initial_balance + 999999.99
    
    # Exact balance boundary tests
    
    @patch('builtins.input', return_value='1000.00')
    def test_debit_exact_balance(self, mock_input, capsys):
        """Test debit with exact balance amount (account should go to zero)"""
        self.acc.debit_account()
        
        assert self.acc.balance == 0.00
        
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['debit'] in captured.out
        assert "0.00" in captured.out
    
    # Precision boundary tests
    
    @patch('builtins.input', return_value='1000.01')
    def test_debit_one_cent_over_balance(self, mock_input, capsys):
        """Test debit one cent more than balance (should be rejected)"""
        initial_balance = self.acc.balance
        self.acc.debit_account()
        
        assert self.acc.balance == initial_balance
        
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['insufficient'] in captured.out