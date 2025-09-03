## Testing

The system includes comprehensive automated tests using pytest. The test suite covers all functionality with 100% code coverage.

### Test Structure

```
tests/
└── test_account_system.py    # Complete test suite
```

### Running Tests

#### Prerequisites
```bash
pip install pytest pytest-cov
```

#### Basic Test Execution
```bash
# Run all tests
python -m pytest test_account_system.py -v

# Run with coverage report
python -m pytest test_account_system.py --cov=. --cov-report=html

# Run specific test class
python -m pytest test_account_system.py::TestDataProgram -v
```

### Test Coverage

#### TestDataProgram
Tests the data storage layer:
- ✅ Initial balance verification (1000.00)
- ✅ READ operation functionality
- ✅ WRITE operation with balance updates
- ✅ WRITE operation without parameters
- ✅ Invalid operation error handling
- ✅ Global function interface

#### TestOperations  
Tests the business logic layer:
- ✅ View balance operations
- ✅ Credit transactions (positive amounts)
- ✅ Debit transactions (sufficient funds)
- ✅ Negative amount validation (credit/debit)
- ✅ Zero amount handling
- ✅ Exact balance debit (results in 0.00)
- ✅ Insufficient funds protection
- ✅ Multiple consecutive operations
- ✅ Invalid operation type handling

#### TestMainProgram
Tests the user interface layer:
- ✅ Menu display and formatting
- ✅ Balance display with correct messaging
- ✅ Credit operation user flow
- ✅ Debit operation user flow
- ✅ Invalid menu choice handling (numeric/non-numeric)
- ✅ Invalid amount input validation
- ✅ Retry prompts for invalid inputs
- ✅ Edge cases (exact balance debit, insufficient funds)
- ✅ Multiple operation sequences
- ✅ Program exit with goodbye message

#### TestIntegration
End-to-end workflow testing:
- ✅ Complete user session simulation
- ✅ Multi-operation sequences with balance verification
- ✅ State persistence across operations


### Test Categories

**Unit Tests**: Each module tested in isolation
- DataProgram: Storage operations
- Operations: Business logic validation  
- MainProgram: User interface handling

**Integration Tests**: End-to-end functionality
- Complete user workflows
- Cross-module communication
- State management verification

**Edge Case Tests**: Boundary conditions
- Zero amounts
- Exact balance operations
- Insufficient funds scenarios
- Invalid input handling


## Limitations

- **Session-Only Persistence**: Balance resets to $1,000.00 on program restart
- **Single Account**: System handles only one account
- **Console Interface**: Text-based interface only
- **No Authentication**: No user login or security features

