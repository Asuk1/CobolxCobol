"""
test_account_integration.py - Integration and full system workflow tests

This module contains end-to-end integration tests that verify complete user workflows:
- Menu system navigation and display
- Combined operations (credit + debit + view + exit)
- Invalid menu choices
- Complete user scenarios from start to finish

These tests simulate real user interactions and ensure all components work together
correctly in realistic usage scenarios.
"""

import pytest
from unittest.mock import patch
from conftest import INITIAL_BALANCE, EXPECTED_MESSAGES


class TestAccountSystemIntegration:
    """
    Integration tests for complete AccountSystem workflows.
    These tests validate end-to-end scenarios equivalent to TestPlan scenarios.
    """
    
    def setup_method(self):
        """Setup before each test - use fresh AccountSystem instance"""
        from accountsystem import AccountSystem
        self.acc = AccountSystem()
        assert self.acc.balance == INITIAL_BALANCE  # Validate setup
    
    # Single operation integration tests
    
    @patch('builtins.input', side_effect=['1', '4'])
    def test_run_view_balance_then_exit(self, mock_input, capsys):
        """TC-4.1: Complete test - view balance then exit"""
        self.acc.run()
        
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['system_title'] in captured.out
        assert f"{EXPECTED_MESSAGES['current_balance']} {INITIAL_BALANCE:.2f}" in captured.out
        assert EXPECTED_MESSAGES['exit_message'] in captured.out
    
    @patch('builtins.input', side_effect=['2', '250.00', '1', '4'])
    def test_run_credit_view_exit(self, mock_input, capsys):
        """Integration test: credit, view balance, exit"""
        self.acc.run()
        
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['credit'] in captured.out
        assert "1250.00" in captured.out
        assert f"{EXPECTED_MESSAGES['current_balance']} 1250.00" in captured.out
        assert EXPECTED_MESSAGES['exit_message'] in captured.out
        
        # Final balance verification
        assert self.acc.balance == 1250.00
    
    @patch('builtins.input', side_effect=['3', '150.00', '1', '4'])
    def test_run_debit_view_exit(self, mock_input, capsys):
        """Integration test: debit, view balance, exit"""
        self.acc.run()
        
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['debit'] in captured.out
        assert "850.00" in captured.out
        assert f"{EXPECTED_MESSAGES['current_balance']} 850.00" in captured.out
        assert EXPECTED_MESSAGES['exit_message'] in captured.out
        
        assert self.acc.balance == 850.00
    
    # Menu validation tests
    
    @patch('builtins.input', side_effect=['5', '4'])
    def test_run_invalid_choice(self, mock_input, capsys):
        """Test invalid menu choice handling"""
        self.acc.run()
        
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['invalid_choice'] in captured.out
        assert EXPECTED_MESSAGES['exit_message'] in captured.out
    
    # Complex multi-operation integration tests
    
    @patch('builtins.input', side_effect=['2', '100.00', '3', '50.00', '1', '4'])
    def test_run_complete_scenario(self, mock_input, capsys):
        """Complete scenario test: credit, debit, view balance, exit"""
        self.acc.run()
        
        captured = capsys.readouterr()
        
        # Credit verifications - should show balance progression
        assert EXPECTED_MESSAGES['credit'] in captured.out
        assert "1100.00" in captured.out
        
        # Debit verifications - should show balance progression  
        assert EXPECTED_MESSAGES['debit'] in captured.out
        assert "1050.00" in captured.out
        
        # Final display verification
        assert f"{EXPECTED_MESSAGES['current_balance']} 1050.00" in captured.out
        assert EXPECTED_MESSAGES['exit_message'] in captured.out
        
        # Final balance verification
        assert self.acc.balance == 1050.00