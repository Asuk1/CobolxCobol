# operations.py - Equivalent to COBOL Operations program
from data_program import call_data_program

class Operations:
    """Operations program - handles all account operations"""

    def call_program(self, operation_type, amount=None):
        """
        Equivalent to COBOL CALL 'Operations' USING operation-type
        """
        if operation_type == 'TOTAL':
            return self._handle_view_balance()
        elif operation_type == 'CREDIT':
            return self._handle_credit(amount)
        elif operation_type == 'DEBIT':
            return self._handle_debit(amount)
        else:
            raise ValueError(f"Invalid operation type: {operation_type}")

    def _handle_view_balance(self):
        """Return current balance"""
        return call_data_program('READ')

    def _handle_credit(self, amount):
        """Apply credit and return new balance"""
        if amount < 0:
            raise ValueError("Amount must be zero or positive.")

        balance = call_data_program('READ')
        balance += amount
        call_data_program('WRITE', balance)
        return balance

    def _handle_debit(self, amount):
        """Apply debit and return new balance if valid"""
        if amount < 0:
            raise ValueError("Amount must be zero or positive.")

        balance = call_data_program('READ')
        if balance >= amount:
            balance -= amount
            call_data_program('WRITE', balance)
            return balance
        else:
            raise ValueError("Insufficient funds for this debit.")
