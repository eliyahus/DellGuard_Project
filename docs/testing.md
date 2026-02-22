# Testing Guide

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suites

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Specific test file
pytest tests/unit/test_guard_system.py -v

# Specific test function
pytest tests/unit/test_guard_system.py::test_threshold_calculation -v
```

### Test Coverage

```bash
# Generate coverage report
pytest tests/ --cov=src --cov-report=html

# View report
open htmlcov/index.html
```

## Test Structure

```
tests/
├── conftest.py           # Shared fixtures
├── constants.py          # Test constants
├── unit/                 # Unit tests
│   ├── test_ai_providers.py
│   ├── test_config.py
│   ├── test_data_loaders.py
│   ├── test_exceptions.py
│   ├── test_guard_system.py
│   ├── test_metrics.py
│   └── test_models.py
└── integration/          # Integration tests
    └── test_guard_workflow.py
```

## Test Coverage

- **Unit Tests**: 35 tests
  - AI providers (3 tests)
  - Configuration (2 tests)
  - Data loaders (4 tests)
  - Exceptions (7 tests)
  - Guard system (5 tests)
  - Metrics (7 tests)
  - Models (7 tests)

- **Integration Tests**: 7 tests
  - Full workflow without breach
  - Full workflow with breach
  - Threshold calculation
  - Metrics tracking

## Writing Tests

### Using Fixtures

```python
def test_guard_system_with_fixtures(guard_system):
    """Test using the guard_system fixture"""
    threshold = guard_system.calculate_threshold()
    assert threshold.cpu_threshold > 0
```

Available fixtures (from `conftest.py`):
- `mock_data_loader` - MockDataLoader instance
- `mock_ai_provider` - MockAIProvider instance
- `console_reporter` - ConsoleReporter instance
- `guard_system` - Fully configured GuardSystem

### Using Constants

```python
from tests.constants import TEST_BASELINE_MEAN, TEST_SIGMA

def test_with_constants():
    """Test using shared constants"""
    loader = MockDataLoader(mean=TEST_BASELINE_MEAN, std=5.0)
    # ...
```

### Testing Exceptions

```python
import pytest
from src.utils.exceptions import DataLoadError

def test_data_load_error():
    """Test exception handling"""
    loader = CSVDataLoader(Path("nonexistent.csv"))
    
    with pytest.raises(DataLoadError, match="Data file not found"):
        loader.load_baseline_data()
```

## Test Best Practices

1. **Use descriptive test names** - `test_threshold_calculation_with_valid_data`
2. **One assertion per test** - Keep tests focused
3. **Use fixtures** - Avoid duplicate setup code
4. **Use constants** - No magic numbers in tests
5. **Test edge cases** - Empty data, invalid input, etc.
6. **Mock external dependencies** - Don't call real AI services in tests

## Continuous Integration

Tests run automatically on:
- Every commit
- Pull requests
- Before deployment

All tests must pass before merging.

## Performance

- **Execution time**: ~0.5s for all 42 tests
- **No external dependencies**: All tests use mocks
- **Fast feedback**: Quick iteration cycle
