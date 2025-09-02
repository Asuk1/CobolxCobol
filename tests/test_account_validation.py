"""
test_account_validation_simple.py - Tests de validation d'entrée simplifiés
"""
import pytest
from unittest.mock import patch
from conftest import INITIAL_BALANCE, EXPECTED_MESSAGES


class TestAccountValidationSimple:
    """Tests de validation simplifiés pour AccountSystem."""
    
    def setup_method(self):
        """Setup avant chaque test"""
        from accountsystem import AccountSystem
        self.acc = AccountSystem()
        assert self.acc.balance == INITIAL_BALANCE

    @patch('builtins.input', return_value='100.00')
    def test_credit_valid_input(self, mock_input):
        """Test crédit avec entrée valide"""
        initial_balance = self.acc.balance
        self.acc.credit_account()
        assert self.acc.balance == initial_balance + 100.00

    @patch('builtins.input', return_value='50.50')
    def test_debit_valid_input(self, mock_input):
        """Test débit avec entrée valide"""
        initial_balance = self.acc.balance
        self.acc.debit_account()
        assert self.acc.balance == initial_balance - 50.50

 
    @patch('builtins.input', return_value='abc')
    def test_credit_invalid_format(self, mock_input, capsys):
        """Test crédit avec format invalide"""
        initial_balance = self.acc.balance
        self.acc.credit_account()
        
        # Le solde ne devrait pas changer
        assert self.acc.balance == initial_balance
        
        # Vérifier le message d'erreur
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['invalid_input'] in captured.out

    @patch('builtins.input', return_value='1000.00')
    def test_debit_insufficient_funds(self, mock_input, capsys):
        """Test débit avec fonds insuffisants"""
        initial_balance = self.acc.balance
        self.acc.debit_account()
        
        # Le solde ne devrait pas changer
        assert self.acc.balance == initial_balance
        
        # Vérifier le message d'erreur
        captured = capsys.readouterr()
        assert EXPECTED_MESSAGES['insufficient_funds'] in captured.out

    def test_get_balance(self):
        """Test obtention du solde"""
        balance = self.acc.get_balance()
        assert balance == INITIAL_BALANCE
        assert isinstance(balance, float)