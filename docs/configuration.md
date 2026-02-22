# Configuration Guide

## Configuration Files

DellGuard uses YAML configuration files located in the `config/` directory.

### Default Configuration

`config/default.yaml`:

```yaml
monitoring:
  threshold_sigma: 3.0  # 3-sigma = 99.7% confidence interval

ai:
  provider: "ollama"
  model: "llama3"

data:
  metrics_file: "server_metrics.csv"
  baseline_status: "Normal"

logging:
  level: "INFO"
  file: "incidents.log"
  format: "json"
```

## Environment Variables

Environment variables override configuration file values:

```bash
# Monitoring
export DELLGUARD_THRESHOLD_SIGMA=2.5

# AI Configuration
export DELLGUARD_AI_PROVIDER=ollama
export DELLGUARD_AI_MODEL=llama3.1

# Data
export DELLGUARD_METRICS_FILE=data/metrics.csv
export DELLGUARD_BASELINE_STATUS=Healthy

# Logging
export DELLGUARD_LOG_LEVEL=DEBUG
export DELLGUARD_LOG_FILE=logs/incidents.log
export DELLGUARD_LOG_FORMAT=json
```

## Configuration Options

### Monitoring

- **threshold_sigma** (float): Number of standard deviations for threshold
  - `2.0` = 95.4% confidence (more sensitive)
  - `3.0` = 99.7% confidence (default, balanced)
  - `4.0` = 99.99% confidence (less sensitive)

### AI Provider

- **provider** (string): AI provider to use
  - `ollama` - Local Ollama instance
  - `mock` - Mock provider for testing

- **model** (string): AI model name
  - `llama3` - Llama 3 8B (default)
  - `llama3.1` - Llama 3.1 8B
  - Any Ollama-supported model

### Data

- **metrics_file** (string): Path to metrics CSV file
- **baseline_status** (string): Status value for baseline data (e.g., "Normal", "Healthy")

### Logging

- **level** (string): Log level
  - `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

- **file** (string): Log file path
- **format** (string): Log format
  - `json` - Structured JSON logs (recommended)
  - `text` - Plain text logs

## Custom Configuration

Create a custom configuration file:

```yaml
# config/production.yaml
monitoring:
  threshold_sigma: 2.5

ai:
  provider: "ollama"
  model: "llama3.1"

logging:
  level: "WARNING"
  file: "/var/log/dellguard/incidents.log"
```

Load it programmatically:

```python
from src.utils.config import Config

config = Config(config_path="config/production.yaml")
```

## Best Practices

1. **Use environment variables for secrets** - Never commit credentials to config files
2. **Keep default.yaml generic** - Environment-specific values in env vars
3. **Document custom settings** - Add comments to explain non-obvious values
4. **Test configuration changes** - Run tests after modifying config
