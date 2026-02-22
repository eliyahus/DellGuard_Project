# Architecture Overview

## System Design

DellGuard follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         Entry Point (monitor.py)        │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Core Layer (GuardSystem)        │
│  - Monitoring loop                      │
│  - Threshold calculation                │
│  - Incident detection                   │
└──┬──────────────┬──────────────┬────────┘
   │              │              │
   ▼              ▼              ▼
┌──────┐    ┌──────────┐   ┌──────────┐
│ Data │    │    AI    │   │ Reporting│
│Layer │    │  Layer   │   │  Layer   │
└──────┘    └──────────┘   └──────────┘
```

## Core Components

### GuardSystem (src/core/monitor.py)
The main orchestrator that:
- Calculates thresholds from baseline data
- Monitors server metrics in real-time
- Detects anomalies using 3-sigma rule
- Triggers AI analysis on breach
- Initiates rollback procedures

### Data Layer (src/data/)
- **DataLoader**: Abstract interface for loading baseline data
- **CSVDataLoader**: Loads data from CSV files
- **MockDataLoader**: Test implementation
- **Models**: Type-safe dataclasses (ServerMetrics, ThresholdConfig, IncidentReport)

### AI Layer (src/ai/)
- **AIProvider**: Abstract interface for AI analysis
- **OllamaProvider**: Integration with Ollama/Llama3
- **MockAIProvider**: Test implementation
- Includes retry logic and error handling

### Reporting Layer (src/reporting/)
- **IncidentReporter**: Abstract interface for reporting
- **ConsoleReporter**: Prints to console
- **LoggingReporter**: Writes to structured logs
- **PerformanceMetrics**: Tracks system performance
- **Visualizer**: Generates charts

### Utilities (src/utils/)
- **Config**: YAML configuration management
- **Exceptions**: Custom exception hierarchy
- **Retry**: Retry decorator with exponential backoff

## Design Principles

### Dependency Injection
All components use abstract interfaces, allowing:
- Easy testing with mocks
- Swappable implementations
- Loose coupling

### Type Safety
- Full type hints throughout
- Dataclasses for structured data
- Mypy-compatible

### Error Handling
- Custom exception hierarchy
- Graceful degradation
- Retry logic for transient failures

### Configuration
- YAML-based configuration
- Environment variable overrides
- Centralized config access

## Data Flow

1. **Initialization**: Load configuration and create dependencies
2. **Baseline**: Calculate threshold from historical data
3. **Monitoring**: Poll server metrics at regular intervals
4. **Detection**: Compare metrics against threshold
5. **Analysis**: On breach, consult AI for diagnosis
6. **Response**: Log incident and trigger rollback
7. **Reporting**: Generate visualizations and metrics

## Testing Strategy

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test full workflow end-to-end
- **Mocks**: Use mock implementations for external dependencies
- **Fixtures**: Pytest fixtures for common test setup

See [Testing Guide](testing.md) for details.
