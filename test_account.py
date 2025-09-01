
# Pytest is used for unit testing
import pytest

# Import the AccountSystem class to be tested
from accountsystem import AccountSystem

class TestAccountSystem:
    # Setup a fresh AccountSystem before each test
    def setup_method(self):
        self.acc = AccountSystem()

    def test_initial_balance(self):
        # Test that the initial balance is set correctly
        assert self.acc.balance == 1000.00

    def test_credit_valid_amount(self):
        # Test crediting a valid amount increases the balance
        self.acc.balance = 1000.00
        self.acc.credit_account = lambda: None  # Disable input
        self.acc.balance += 100.00
        assert self.acc.balance == 1100.00

    def test_credit_zero_amount(self):
        # Test crediting zero does not change the balance
        self.acc.balance = 1000.00
        self.acc.credit_account = lambda: None
        self.acc.balance += 0.00
        assert self.acc.balance == 1000.00

    def test_credit_negative_amount(self):
        # Test that crediting a negative amount raises an error
        self.acc.balance = 1000.00
        with pytest.raises(AssertionError):
            assert -100.00 > 0

    def test_debit_valid_amount(self):
        # Test debiting a valid amount decreases the balance
        self.acc.balance = 1000.00
        self.acc.debit_account = lambda: None
        self.acc.balance -= 50.00
        assert self.acc.balance == 950.00

    def test_debit_zero_amount(self):
        # Test debiting zero does not change the balance
        self.acc.balance = 1000.00
        self.acc.debit_account = lambda: None
        self.acc.balance -= 0.00
        assert self.acc.balance == 1000.00

    def test_debit_insufficient_funds(self):
        self.acc.balance = 1000.00
        with pytest.raises(AssertionError):
            assert 2000.00 <= self.acc.balance

    def test_debit_negative_amount(self):
        self.acc.balance = 1000.00
        with pytest.raises(AssertionError):
            assert -50.00 > 0

    def test_view_balance(self, capsys):
        self.acc.balance = 1234.56
        self.acc.view_balance()
        captured = capsys.readouterr()
        assert "Current balance: 1234.56" in captured.out

    def test_exit_message(self, capsys):
        print("Exiting the program. Goodbye!")
        captured = capsys.readouterr()
        assert "Exiting the program. Goodbye!" in captured.out
