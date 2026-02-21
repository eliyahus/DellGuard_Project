# Step 8: Code Quality Improvements - Implementation Plan

## Current State Assessment

After completing Steps 1-7, the codebase has:
- ✅ Professional project structure (src/, tests/, tools/)
- ✅ Configuration management (YAML + env overrides)
- ✅ Type hints throughout
- ✅ Dependency injection
- ✅ Structured logging
- ✅ 35 passing tests

## Issues to Address

### 1. Legacy Files (High Priority)

**Old files in root directory that should be removed:**
- `ai_analyzer.py` - Replaced by `src/ai/client.py` and `src/ai/providers.py`
- `analyzer.py` - Replaced by `src/core/analyzer.py`
- `guard.py` - Replaced by `src/core/monitor.py`
- `simulate.py` - Replaced by `tools/simulate.py`
- `visualizer.py` - Replaced by `src/reporting/visualizer.py`

**Action:** Delete these files or move to `legacy/` folder for reference

### 2. Magic Numbers in Production Code

**tools/simulate.py:**
```python
# Current
self.normal_cpu = 40.0
self.normal_latency = 100.0
self.normal_errors = 0.02
self.noise_level = 0.05
cpu = self.normal_cpu * (2.5 + noise)  # Magic multipliers
latency = self.normal_latency * (5 + noise)
errors = self.normal_errors * (10 + noise)
```

**Should be:**
```python
# Constants at module level
NORMAL_CPU_PERCENT = 40.0
NORMAL_LATENCY_MS = 100.0
NORMAL_ERROR_RATE = 0.02
NOISE_LEVEL = 0.05

# Incident multipliers
CPU_SPIKE_MULTIPLIER = 2.5
LATENCY_SPIKE_MULTIPLIER = 5.0
ERROR_SPIKE_MULTIPLIER = 10.0
```

**src/core/monitor.py:**
```python
# Current
has_incident: bool = i >= 6  # Magic number
print("="*50)  # Magic number

# Should be
INCIDENT_START_STEP = 6
SEPARATOR_WIDTH = 50
```

### 3. Magic Numbers in Tests

**tests/integration/test_guard_workflow.py:**
- `mean=40.0, std=5.0` - Repeated across tests
- `sigma=3.0` - Standard test sigma
- `steps=5, steps=10` - Test iteration counts
- `i >= 6` - Breach step number

**tests/unit/test_data_loaders.py:**
- `mean=40.0, std=5.0, mean=50.0, std=10.0, mean=45.0, std=7.5`

**tests/unit/test_metrics.py:**
- `duration_ms=1500.0, 1000.0, 500.0`
- `time.sleep(0.01)`
- Calculated values: `0.2, 0.667, 1000.0`

**Solution:** Create `tests/constants.py`:
```python
# Test baseline data
TEST_BASELINE_MEAN = 40.0
TEST_BASELINE_STD = 5.0
TEST_SIGMA = 3.0
TEST_EXPECTED_THRESHOLD = 55.0  # mean + (sigma * std)

# Alternative test values
TEST_BASELINE_MEAN_ALT = 50.0
TEST_BASELINE_STD_ALT = 10.0

# Monitoring steps
TEST_STEPS_SHORT = 5
TEST_STEPS_FULL = 10
TEST_BREACH_STEP = 6

# AI call durations
TEST_AI_DURATION_FAST_MS = 500.0
TEST_AI_DURATION_NORMAL_MS = 1000.0
TEST_AI_DURATION_SLOW_MS = 1500.0

# Test timing
TEST_SLEEP_DURATION_S = 0.01
```

### 4. Missing Documentation

**Modules without docstrings:**
- `src/ai/__init__.py` - Empty, should have module docstring
- `src/core/__init__.py` - Empty
- `src/data/__init__.py` - Empty
- `src/reporting/__init__.py` - Empty
- `src/utils/__init__.py` - Empty

**Add to each:**
```python
"""
Module description here.

This module provides...
"""
```

### 5. Code Duplication

**Test setup duplication:**
```python
# Repeated in multiple test files
data_loader = MockDataLoader(mean=40.0, std=5.0)
ai_provider = MockAIProvider()
reporter = ConsoleReporter()
```

**Solution:** Create `tests/conftest.py` with fixtures:
```python
import pytest
from src.ai.providers import MockAIProvider
from src.data.loader import MockDataLoader
from src.reporting.reporter import ConsoleReporter
from tests.constants import TEST_BASELINE_MEAN, TEST_BASELINE_STD

@pytest.fixture
def mock_data_loader():
    return MockDataLoader(mean=TEST_BASELINE_MEAN, std=TEST_BASELINE_STD)

@pytest.fixture
def mock_ai_provider():
    return MockAIProvider()

@pytest.fixture
def console_reporter():
    return ConsoleReporter()

@pytest.fixture
def guard_system(mock_data_loader, mock_ai_provider, console_reporter):
    from src.core.monitor import GuardSystem
    return GuardSystem(
        data_loader=mock_data_loader,
        ai_provider=mock_ai_provider,
        reporter=console_reporter,
        sigma=TEST_SIGMA
    )
```

### 6. Inconsistent Naming

**Variable names that could be improved:**
- `i` in loops → `step_number` or `step`
- `df` → `metrics_df` or `baseline_df`
- `e` in exceptions → `error` or specific name

### 7. Missing Type Hints

**Test functions missing return types:**
```python
# Current
def test_something():
    pass

# Should be
def test_something() -> None:
    pass
```

### 8. Code Comments

**Areas needing better comments:**
- Why `INCIDENT_START_STEP = 6` specifically?
- Why certain multipliers in simulator?
- Why specific sigma values in tests?

## Implementation Plan

### Phase 1: Cleanup (High Priority)
1. Create `tests/constants.py` with all test constants
2. Create `tests/conftest.py` with pytest fixtures
3. Move old root files to `legacy/` folder
4. Add `.gitignore` entry for `legacy/`

### Phase 2: Extract Constants (High Priority)
5. Extract magic numbers from `tools/simulate.py`
6. Extract magic numbers from `src/core/monitor.py`
7. Update all test files to use constants from `tests/constants.py`

### Phase 3: Documentation (Medium Priority)
8. Add module docstrings to all `__init__.py` files
9. Add comments explaining "why" for magic numbers
10. Document test data choices in `tests/constants.py`

### Phase 4: Refactor Tests (Medium Priority)
11. Update tests to use pytest fixtures
12. Add return type hints to all test functions
13. Improve variable names in tests

### Phase 5: Polish (Low Priority)
14. Improve variable names in production code
15. Add more descriptive comments
16. Consider parametrized tests for similar cases

## Success Criteria

- All 35 tests still pass
- No magic numbers in production code
- No magic numbers in test assertions
- All modules have docstrings
- Test setup uses fixtures
- Legacy files removed or archived
- Code is more maintainable and readable

## Commands to Run

```bash
# Run tests after each change
pytest tests/ -v

# Check for issues
flake8 src/ tests/  # If installed
mypy src/  # Type checking

# Clean up
mkdir legacy
mv ai_analyzer.py analyzer.py guard.py simulate.py visualizer.py legacy/
```

## Notes

- Make changes incrementally
- Run tests after each phase
- Keep commits focused on one type of change
- Document why constants have specific values
- Balance DRY principle with readability
