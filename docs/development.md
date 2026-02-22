# Development Guide

## Getting Started

### Prerequisites

- Python 3.12+
- pip
- git

### Setup Development Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests to verify setup
pytest tests/ -v
```

## Project Structure

```
DellGuard/
├── src/                  # Production code
│   ├── ai/              # AI provider implementations
│   ├── core/            # Core monitoring logic
│   ├── data/            # Data models and loaders
│   ├── reporting/       # Logging and metrics
│   └── utils/           # Utilities (config, exceptions, retry)
├── tests/               # Test suite
├── config/              # Configuration files
├── tools/               # Utilities (simulator)
├── docs/                # Documentation
```

## Extending DellGuard

### Adding a New AI Provider

1. Create a new class implementing `AIProvider`:

```python
# src/ai/providers.py
from src.ai.providers import AIProvider
from src.utils.retry import retry
from src.utils.exceptions import AIProviderError

class CustomAIProvider(AIProvider):
    """Custom AI provider implementation"""
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
    
    @retry(max_attempts=3, delay=1.0, backoff=2.0)
    def analyze(self, prompt: str) -> str:
        """Analyze using custom AI service"""
        try:
            # Your implementation
            response = your_ai_service.call(prompt)
            return response.text
        except Exception as e:
            raise AIProviderError(f"Custom AI failed: {e}")
```

2. Add configuration:

```yaml
# config/default.yaml
ai:
  provider: "custom"
  api_key: "${CUSTOM_AI_KEY}"
```

3. Add tests:

```python
# tests/unit/test_ai_providers.py
def test_custom_ai_provider():
    provider = CustomAIProvider(api_key="test-key")
    result = provider.analyze("test prompt")
    assert isinstance(result, str)
```

### Adding a New Data Loader

1. Implement `DataLoader` interface:

```python
# src/data/loader.py
from src.data.loader import DataLoader
from src.utils.exceptions import DataLoadError

class DatabaseDataLoader(DataLoader):
    """Load baseline from database"""
    
    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
    
    def load_baseline_data(self) -> Tuple[float, float]:
        """Load baseline from database"""
        try:
            # Your implementation
            conn = connect(self.connection_string)
            mean, std = query_baseline(conn)
            return mean, std
        except Exception as e:
            raise DataLoadError(f"Database load failed: {e}")
```

2. Add tests with fixtures.

### Adding a New Reporter

```python
# src/reporting/reporter.py
class SlackReporter(IncidentReporter):
    """Send incidents to Slack"""
    
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url
    
    def report_incident(self, incident: IncidentReport) -> None:
        """Send incident to Slack"""
        message = self._format_message(incident)
        requests.post(self.webhook_url, json={"text": message})
```

## Code Style

### Type Hints

Always use type hints:

```python
def calculate_threshold(mean: float, std: float, sigma: float) -> float:
    """Calculate threshold value"""
    return mean + (sigma * std)
```

### Docstrings

Use Google-style docstrings:

```python
def analyze_incident(cpu: float, threshold: float) -> str:
    """
    Analyze incident using AI.
    
    Args:
        cpu: Current CPU usage percentage
        threshold: Threshold value
        
    Returns:
        AI diagnosis string
        
    Raises:
        AIProviderError: If AI analysis fails
    """
```

### Error Handling

Use custom exceptions:

```python
from src.utils.exceptions import DataLoadError

try:
    data = load_data()
except FileNotFoundError:
    raise DataLoadError("Data file not found")
```

## Testing Requirements

- All new features must have tests
- Maintain 100% test pass rate
- Use fixtures for common setup
- Use constants instead of magic numbers
- Mock external dependencies

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and add tests
3. Run tests: `pytest tests/ -v`
4. Commit with descriptive message
5. Push and create pull request
6. Ensure CI passes
7. Request review

## Commit Message Format

```
type: brief description

- Detailed change 1
- Detailed change 2
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

## Resources

- [Architecture Overview](architecture.md)
- [Configuration Guide](configuration.md)
- [Testing Guide](testing.md)
- [Refactoring Journey](refactoring/)
