# test_account_system.py - Comprehensive pytest tests for loosely coupled account system
import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

# Import the modules (adjust imports based on your actual file structure)
from data_program import DataProgram, call_data_program, _data_program_instance
from operations import Operations
from main import MainProgram

class TestDataProgram:
    """Test the DataProgram class - data storage functionality"""
    
    def setup_method(self):
        """Reset data program state before each test"""
        self.data_program = DataProgram()
    
    def test_initial_balance_is_1000(self):
        """Test that initial balance is set correctly to 1000.00"""
        balance = self.data_program.call_program('READ')
        assert balance == 1000.00
    
    def test_read_operation_returns_current_balance(self):
        """Test READ operation returns the stored balance"""
        # Set a specific balance first
        self.data_program.call_program('WRITE', 750.50)
        
        # Read should return the same balance
        balance = self.data_program.call_program('READ')
        assert balance == 750.50
    
    def test_write_operation_updates_balance(self):
        """Test WRITE operation updates the stored balance"""
        new_balance = 1250.75
        result = self.data_program.call_program('WRITE', new_balance)
        
        # Should return the new balance
        assert result == new_balance
        
        # Reading should return the same value
        stored_balance = self.data_program.call_program('READ')
        assert stored_balance == new_balance
    
    def test_write_operation_without_balance_parameter(self):
        """Test WRITE operation without balance parameter"""
        # Should not crash and should return current balance
        current_balance = self.data_program.call_program('READ')
        result = self.data_program.call_program('WRITE')
        assert result == current_balance
    
    def test_invalid_operation_raises_error(self):
        """Test invalid operation type raises ValueError"""
        with pytest.raises(ValueError, match="Invalid operation type"):
            self.data_program.call_program('INVALID')
    
    def test_global_call_data_program_function(self):
        """Test the global call_data_program function works correctly"""
        # Reset global instance
        global _data_program_instance
        _data_program_instance._storage_balance = 1000.00
        
        # Test READ
        balance = call_data_program('READ')
        assert balance == 1000.00
        
        # Test WRITE
        call_data_program('WRITE', 500.00)
        new_balance = call_data_program('READ')
        assert new_balance == 500.00


class TestOperations:
    """Test the Operations class - business logic functionality"""
    
    def setup_method(self):
        """Reset state before each test"""
        self.operations = Operations()
        # Reset global data program instance
        global _data_program_instance
        _data_program_instance._storage_balance = 1000.00
    
    # BASIC FUNCTIONALITY TESTS
    def test_view_balance_returns_current_balance(self):
        """Test viewing balance returns the current balance"""
        balance = self.operations.call_program('TOTAL')
        assert balance == 1000.00
    
    def test_credit_valid_amount_updates_balance(self):
        """Test crediting a valid amount updates the balance correctly"""
        new_balance = self.operations.call_program('CREDIT', 100.00)
        assert new_balance == 1100.00
        
        # Verify balance is persisted
        current_balance = self.operations.call_program('TOTAL')
        assert current_balance == 1100.00
    
    def test_debit_valid_amount_updates_balance(self):
        """Test debiting a valid amount updates the balance correctly"""
        new_balance = self.operations.call_program('DEBIT', 50.00)
        assert new_balance == 950.00
        
        # Verify balance is persisted
        current_balance = self.operations.call_program('TOTAL')
        assert current_balance == 950.00
    
    # VALIDATION TESTS
    def test_credit_negative_amount_raises_error(self):
        """Test crediting negative amount raises validation error"""
        with pytest.raises(ValueError, match="Amount must be zero or positive"):
            self.operations.call_program('CREDIT', -50.00)
    
    def test_debit_negative_amount_raises_error(self):
        """Test debiting negative amount raises validation error"""
        with pytest.raises(ValueError, match="Amount must be zero or positive"):
            self.operations.call_program('DEBIT', -25.00)
    
    def test_credit_zero_amount_is_allowed(self):
        """Test crediting zero amount is allowed"""
        original_balance = self.operations.call_program('TOTAL')
        new_balance = self.operations.call_program('CREDIT', 0.00)
        assert new_balance == original_balance
    
    def test_debit_zero_amount_is_allowed(self):
        """Test debiting zero amount is allowed"""
        original_balance = self.operations.call_program('TOTAL')
        new_balance = self.operations.call_program('DEBIT', 0.00)
        assert new_balance == original_balance
    
    # EDGE CASES
    def test_debit_exactly_equal_to_balance_leaves_zero(self):
        """Test debiting exact balance amount leaves balance at zero"""
        current_balance = self.operations.call_program('TOTAL')
        new_balance = self.operations.call_program('DEBIT', current_balance)
        assert new_balance == 0.00
    
    def test_debit_larger_than_balance_raises_insufficient_funds(self):
        """Test debiting more than balance raises insufficient funds error"""
        current_balance = self.operations.call_program('TOTAL')
        with pytest.raises(ValueError, match="Insufficient funds for this debit"):
            self.operations.call_program('DEBIT', current_balance + 100.00)
    
    def test_multiple_consecutive_operations_maintain_correct_balance(self):
        """Test multiple consecutive credits and debits maintain correct balance"""
        # Starting balance: 1000.00
        
        # Credit 200.00 -> 1200.00
        balance1 = self.operations.call_program('CREDIT', 200.00)
        assert balance1 == 1200.00
        
        # Debit 300.00 -> 900.00
        balance2 = self.operations.call_program('DEBIT', 300.00)
        assert balance2 == 900.00
        
        # Credit 150.00 -> 1050.00
        balance3 = self.operations.call_program('CREDIT', 150.00)
        assert balance3 == 1050.00
        
        # Debit 50.00 -> 1000.00
        final_balance = self.operations.call_program('DEBIT', 50.00)
        assert final_balance == 1000.00
    
    def test_invalid_operation_type_raises_error(self):
        """Test invalid operation type raises ValueError"""
        with pytest.raises(ValueError, match="Invalid operation type"):
            self.operations.call_program('INVALID')


class TestMainProgram:
    """Test the MainProgram class - user interface functionality"""
    
    def setup_method(self):
        """Reset state before each test"""
        # Reset global data program instance
        global _data_program_instance
        _data_program_instance._storage_balance = 1000.00
        self.main_program = MainProgram()
    
    # BASIC FUNCTIONALITY TESTS
    def test_view_balance_displays_correct_message(self, monkeypatch, capfd):
        """Test viewing balance displays correct COBOL-equivalent message"""
        # Mock user input: choice 1 (view balance), then 4 (exit)
        inputs = iter(['1', '4'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        assert "Current balance: 1000.00" in captured.out
        assert "Exiting the program. Goodbye!" in captured.out
    
    def test_credit_with_valid_amount_displays_correct_message(self, monkeypatch, capfd):
        """Test credit with valid amount displays COBOL-equivalent message"""
        # Mock user input: choice 2 (credit), amount 100, then 4 (exit)
        inputs = iter(['2', '100.00', '4'])
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        assert "Amount credited. New balance: 1100.00" in captured.out
        assert "Exiting the program. Goodbye!" in captured.out
    
    def test_debit_with_valid_amount_displays_correct_message(self, monkeypatch, capfd):
        """Test debit with valid amount displays COBOL-equivalent message"""
        # Mock user input: choice 3 (debit), amount 50, then 4 (exit)
        inputs = iter(['3', '50.00', '4'])
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        assert "Amount debited. New balance: 950.00" in captured.out
        assert "Exiting the program. Goodbye!" in captured.out
    
    # VALIDATION TESTS
    def test_invalid_menu_choice_numeric_displays_error(self, monkeypatch, capfd):
        """Test invalid numeric menu choice displays error message"""
        # Mock user input: choice 5 (invalid), then 4 (exit)
        inputs = iter(['5', '4'])
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        assert "Invalid choice, please select 1-4." in captured.out
    
    def test_invalid_menu_choice_non_numeric_prompts_retry(self, monkeypatch, capfd):
        """Test non-numeric menu choice prompts for retry with error message"""
        # Mock user input: 'abc' (invalid), then 1 (valid), then 4 (exit)
        inputs = iter(['abc', '1', '4'])
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        assert "Invalid input, please enter a number between 1 and 4." in captured.out
        assert "Current balance: 1000.00" in captured.out  # Should eventually show balance
    
    def test_negative_credit_amount_displays_error(self, monkeypatch, capfd):
        """Test negative credit amount displays validation error"""
        # Mock user input: choice 2 (credit), amount -50 (invalid), then 4 (exit)
        inputs = iter(['2', '-50', '4'])

        def fake_input(prompt):
            try:
                return next(inputs)
            except StopIteration:
                return '4'  # Par défaut, sortir du programme

        monkeypatch.setattr('builtins.input', fake_input)
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        assert "Amount must be zero or positive." in captured.out
        assert "Exiting the program. Goodbye!" in captured.out

    def test_negative_debit_amount_displays_error(self, monkeypatch, capfd):
        """Test negative debit amount displays validation error"""
        # Mock user input: choice 3 (debit), amount -25 (invalid), then 4 (exit)
        inputs = iter(['3', '-25', '4'])

        def fake_input(prompt):
            try:
                return next(inputs)
            except StopIteration:
                return '4'  # Par défaut, sortir du programme

        monkeypatch.setattr('builtins.input', fake_input)
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        assert "Amount must be zero or positive." in captured.out
        assert "Exiting the program. Goodbye!" in captured.out

    
    def test_non_numeric_amount_input_prompts_retry(self, monkeypatch, capfd):
        """Test non-numeric amount input prompts for retry with error message"""
        # Mock user input: choice 2 (credit), 'abc' (invalid), 100 (valid), then 4 (exit)
        inputs = iter(['2', 'abc', '100', '4'])
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        assert "Invalid amount, please enter a valid number." in captured.out
        assert "Amount credited. New balance: 1100.00" in captured.out
    
    # EDGE CASES
    def test_debit_exactly_equal_to_balance_shows_zero_balance(self, monkeypatch, capfd):
        """Test debit exactly equal to current balance shows zero balance"""
        # Mock user input: choice 3 (debit), amount 1000 (exact balance), then 4 (exit)
        inputs = iter(['3', '1000.00', '4'])
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        assert "Amount debited. New balance: 0.00" in captured.out
    
    def test_debit_larger_than_balance_shows_insufficient_funds(self, monkeypatch, capfd):
        """Test debit larger than balance shows COBOL-equivalent insufficient funds message"""
        # Mock user input: choice 3 (debit), amount 1500 (exceeds balance), then 4 (exit)
        inputs = iter(['3', '1500.00', '4'])
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        assert "Insufficient funds for this debit." in captured.out
    
    def test_multiple_operations_show_correct_final_balance(self, monkeypatch, capfd):
        """Test multiple consecutive operations show correct final balance"""
        # Multiple operations: credit 200, debit 150, credit 50, view balance, exit
        inputs = iter(['2', '200', '3', '150', '2', '50', '1', '4'])
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        output_lines = captured.out.split('\n')
        
        # Check the sequence of balance updates
        assert any("Amount credited. New balance: 1200.00" in line for line in output_lines)
        assert any("Amount debited. New balance: 1050.00" in line for line in output_lines)
        assert any("Amount credited. New balance: 1100.00" in line for line in output_lines)
        assert any("Current balance: 1100.00" in line for line in output_lines)
    
    def test_menu_display_shows_correct_format(self, monkeypatch, capfd):
        """Test menu displays in correct COBOL-equivalent format"""
        # Mock user input: immediate exit
        inputs = iter(['4'])
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        expected_menu_lines = [
            "--------------------------------",
            "Account Management System",
            "1. View Balance",
            "2. Credit Account",
            "3. Debit Account", 
            "4. Exit",
            "--------------------------------"
        ]
        
        for line in expected_menu_lines:
            assert line in captured.out
    
    def test_exit_option_terminates_program_with_goodbye_message(self, monkeypatch, capfd):
        """Test exit option terminates program with COBOL-equivalent goodbye message"""
        # Mock user input: immediate exit
        inputs = iter(['4'])
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
        
        self.main_program.run()
        
        captured = capfd.readouterr()
        assert "Exiting the program. Goodbye!" in captured.out


class TestIntegration:
    """Integration tests to verify end-to-end functionality"""
    
    def setup_method(self):
        """Reset state before each test"""
        global _data_program_instance
        _data_program_instance._storage_balance = 1000.00
    
    def test_complete_user_session_workflow(self, monkeypatch, capfd):
        """Test a complete user session with all operations"""
        # Simulate a complete session:
        # 1. View initial balance
        # 2. Credit 500
        # 3. View balance  
        # 4. Debit 200
        # 5. View final balance
        # 6. Exit
        inputs = iter(['1', '2', '500', '1', '3', '200', '1', '4'])
        monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
        
        main_program = MainProgram()
        main_program.run()
        
        captured = capfd.readouterr()
        output_lines = captured.out.split('\n')
        
        # Verify the sequence of operations
        balance_displays = [line for line in output_lines if "Current balance:" in line]
        assert len(balance_displays) == 3  # Three balance views
        assert "Current balance: 1000.00" in balance_displays[0]  # Initial
        assert "Current balance: 1500.00" in balance_displays[1]  # After credit
        assert "Current balance: 1300.00" in balance_displays[2]  # After debit
        
        # Verify transaction messages
        assert any("Amount credited. New balance: 1500.00" in line for line in output_lines)
        assert any("Amount debited. New balance: 1300.00" in line for line in output_lines)
        assert any("Exiting the program. Goodbye!" in line for line in output_lines)


# Test configuration
if __name__ == "__main__":
    # Run with: python -m pytest test_account_system.py -v
    # For coverage: python -m pytest test_account_system.py --cov=. --cov-report=html
    pytest.main([__file__, "-v"])