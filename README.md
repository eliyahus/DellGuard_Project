# DellGuard: AI-Driven Infrastructure Safety System 🚀

**DellGuard** is an automated monitoring and safety system designed to protect server infrastructure during software deployments. It uses statistical analysis to detect anomalies and local AI to provide real-time incident diagnostics.

## 🌟 Key Features

* **3-Sigma Statistical Monitoring**: Automatically calculates healthy performance baselines and sets dynamic thresholds
* **AI Incident Diagnosis**: Integrated with **Llama 3 (via Ollama)** to analyze telemetry data and provide human-readable root cause report
* **Automated Rollback Logic**: Instantly triggers safety protocols when critical thresholds are breached

* **Data Visualization**: Generates performance charts (`server_health_chart.png`) for post-incident review
* **Professional Logging**: Maintains a detailed `incidents.log` with AI-generated insights

## 🏗️ Architecture

```
DellGuard/
├── src/
│   ├── ai/           # AI provider abstraction (Ollama, Mock)
│   ├── core/         # Core monitoring logic and analyzers
│   ├── data/         # Data models and loaders
│   ├── reporting/    # Logging, metrics, and visualization
│   └── utils/        # Configuration, exceptions, retry logic
├── tests/
│   ├── unit/         # Unit tests
│   └── integration/  # Integration tests
├── config/           # YAML configuration files
├── tools/            # Simulation and utilities
└── docs/             # Documentation

```

## 🛠 Tech Stack

* **Language:** Python 3.12+
* **Data Analysis:** Pandas, NumPy
* **AI Engine:** Ollama / Llama 3 (8B)
* **Visualization:** Matplotlib
* **Testing:** pytest (42 tests)
* **Configuration:** YAML with environment overrides

## 🚀 Quick Start

### Prerequisites

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install and start Ollama (for AI features)
# Visit: https://ollama.ai
ollama pull llama3
```

### Generate Sample Data

```bash
python tools/simulate.py
# Generates server_metrics.csv with 100 healthy + 10 incident samples
```

### Run Monitoring

```bash
python -m src.core.monitor
# Monitors server metrics and triggers rollback on threshold breach
```

### Run Tests

```bash
pytest tests/ -v
# 42 tests, ~0.5s execution time
```

## 📊 How It Works

1. **Baseline Calculation**: Analyzes historical data to establish normal behavior
   - Calculates mean and standard deviation from healthy samples
   - Applies 3-sigma rule (99.7% confidence interval)

2. **Real-time Monitoring**: Continuously checks server metrics
   - CPU usage
   - Compares against dynamic thresholds

3. **Anomaly Detection**: Triggers on threshold breach
   - Logs breach percentage and severity
   - Records performance metrics

4. **AI Analysis**: Consults AI for root cause diagnosis
   - Retry logic with exponential backoff (3 attempts)
   - Graceful degradation if AI unavailable
   - Structured logging of AI response time

5. **Automated Response**: Initiates rollback procedure
   - Logs incident with AI diagnosis
   - Generates visualization
   - Records metrics for post-mortem

5. **Visualization**: A visual report is generated to show exactly where the spike occurred

## 📸 System in Action
![Server Health Chart](server_health_chart.png)

## 📋 Example AI Diagnosis (from incidents.log)
> "The most likely cause of the rollback is CPU utilization exceeding the threshold (100.30% vs 43.55%). This indicates a critical resource exhaustion, possibly due to a runaway process."

## ⚙️ Configuration

Edit `config/default.yaml`:

```yaml
monitoring:
  threshold_sigma: 3.0        # 3-sigma = 99.7% confidence
  
ai:
  provider: "ollama"
  model: "llama3"
  
logging:
  level: "INFO"
  file: "incidents.log"
  format: "json"
```

Environment variables override config:
```bash
export DELLGUARD_THRESHOLD_SIGMA=2.5
export DELLGUARD_AI_MODEL=llama3.1
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/unit/ -v
pytest tests/integration/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

**Test Coverage:**
- Unit tests: 35 tests (data loaders, models, metrics, exceptions)
- Integration tests: 7 tests (full workflow, AI integration)
- 100% pass rate, ~0.5s execution time

## 📈 Performance Metrics

The system tracks:
- Total health checks performed
- Threshold breaches detected
- AI call success/failure rates
- AI response times (p50, p95, p99)
- System uptime

Access via `guard.metrics.get_summary()`

## 🔧 Development

### Project Structure

- **Dependency Injection**: Abstract interfaces for testability
- **Type Safety**: Full type hints with dataclasses
- **Error Handling**: Custom exceptions with retry logic
- **Logging**: Structured JSON logs with context
- **Configuration**: YAML-based with env overrides

### Adding New AI Providers

```python
from src.ai.providers import AIProvider

class CustomAIProvider(AIProvider):
    def analyze(self, prompt: str) -> str:
        # Your implementation
        return "AI response"
```

### Adding New Data Loaders

```python
from src.data.loader import DataLoader

class CustomDataLoader(DataLoader):
    def load_baseline_data(self) -> Tuple[float, float]:
        # Return (mean, std)
        return 40.0, 5.0
```

## 📚 Documentation

- **[Documentation Index](docs/)** - Complete documentation hub
- **[Architecture Overview](docs/architecture.md)** - System design and components
- **[Configuration Guide](docs/configuration.md)** - Setup and configuration
- **[Testing Guide](docs/testing.md)** - Running and writing tests
- **[Development Guide](docs/development.md)** - Contributing and extending
- **[Refactoring Journey](docs/refactoring/)** - Prototype to production transformation

## 🚀 Roadmap

### Completed ✅
- [x] Professional architecture with src/ layout
- [x] Type safety with dataclasses
- [x] Comprehensive error handling
- [x] Retry logic for AI calls
- [x] Structured logging and metrics
- [x] Test coverage
- [x] Configuration management

### Planned 🔮
- [ ] Multi-metric correlation (CPU + RAM + Latency)
- [ ] Slack/Telegram notifications
- [ ] Predictive anomaly detection
- [ ] Time-series database integration (InfluxDB)
- [ ] Web dashboard for real-time monitoring
- [ ] Kubernetes deployment manifests
