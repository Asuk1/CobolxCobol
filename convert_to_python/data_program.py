# data_program.py - Equivalent to COBOL DataProgram
class DataProgram:
    """Data storage program - manages persistent balance storage"""

    def __init__(self):
        self._storage_balance = 1000.00

    def call_program(self, operation_type, balance=None):
        """
        Equivalent to COBOL CALL 'DataProgram' USING operation, balance
        """
        if operation_type == 'READ':
            return self._storage_balance
        elif operation_type == 'WRITE':
            if balance is not None:
                self._storage_balance = balance
            return self._storage_balance
        else:
            raise ValueError(f"Invalid operation type: {operation_type}")


# Global instance to simulate COBOL persistence
_data_program_instance = DataProgram()


def call_data_program(operation_type, balance=None):
    """Global function to call DataProgram - simulates COBOL CALL statement"""
    return _data_program_instance.call_program(operation_type, balance)
