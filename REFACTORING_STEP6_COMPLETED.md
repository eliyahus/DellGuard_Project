# Refactoring Step 6: Logging & Observability - COMPLETED

## Changes Made

### 1. Structured Logging Module

**src/reporting/logger.py** - Advanced logging with structured data:

```python
class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging"""
    # Adds key=value pairs to log messages

def setup_logging(log_file, log_level, log_format) -> logging.Logger:
    """Setup structured logging with file and console handlers"""

def log_with_context(logger, level, message, **kwargs):
    """Log message with structured context data"""

# Helper functions for common log patterns:
- log_threshold_breach()
- log_system_start()
- log_ai_analysis()
- log_incident()
```

### 2. Performance Metrics Module

**src/reporting/metrics.py** - Track system performance:

```python
@dataclass
class PerformanceMetrics:
    """Track performance metrics for monitoring"""
    total_checks: int
    threshold_breaches: int
    ai_calls: int
    ai_failures: int
    total_ai_duration_ms: float
    
    def get_summary() -> Dict[str, Any]:
        # Returns uptime, breach rate, AI success rate, etc.

class Timer:
    """Context manager for timing operations"""
    # Use with 'with Timer() as timer:' pattern
```

### 3. Enhanced GuardSystem

**src/core/monitor.py** - Integrated logging and metrics:

- Added `PerformanceMetrics` tracking
- Structured logging for all events
- AI call timing with `Timer` context manager
- Metrics summary on completion
- Enhanced error handling with metrics

### 4. Log Output Examples

**Before (Basic logging):**
```
2026-02-21 19:00:00 - INFO - Threshold set to: 55.00%
2026-02-21 19:00:05 - WARNING - THRESHOLD BREACHED: CPU reached 98.50%
```

**After (Structured logging):**
```
2026-02-21 19:00:00 - dellguard - INFO - Guard system initialized | threshold=55.00% | sigma=3.0 | status=active
2026-02-21 19:00:05 - dellguard - WARNING - THRESHOLD BREACHED | cpu_usage=98.50% | threshold=55.00% | breach_percentage=79.1% | severity=high
2026-02-21 19:00:06 - dellguard - INFO - AI analysis completed | duration_ms=1250.50 | success=True
2026-02-21 19:00:06 - dellguard - ERROR - INCIDENT DETECTED - Automatic rollback initiated | cpu_usage=98.50% | threshold=55.00% | action=AUTOMATIC ROLLBACK
2026-02-21 19:00:06 - dellguard - INFO - Performance metrics: {'uptime_seconds': 6.2, 'total_checks': 6, 'threshold_breaches': 1, 'breach_rate': 0.167, 'ai_calls': 1, 'ai_failures': 0, 'ai_success_rate': 1.0, 'avg_ai_duration_ms': 1250.5}
```

## Benefits Achieved

✅ **Structured Logging**: Key-value pairs for easy parsing
✅ **Performance Tracking**: Metrics for uptime, breach rate, AI performance
✅ **Timing Information**: Track AI call duration
✅ **Better Debugging**: Rich context in every log entry
✅ **Observability**: Easy to integrate with log aggregation tools
✅ **Metrics Summary**: Performance report at end of monitoring

## Structured Data Fields

### System Start
- `threshold`: Calculated threshold value
- `sigma`: Sigma multiplier used
- `status`: System status (active)

### Threshold Breach
- `cpu_usage`: Current CPU usage
- `threshold`: Threshold value
- `breach_percentage`: Percentage over threshold
- `severity`: Breach severity level

### AI Analysis
- `duration_ms`: Time taken for AI call
- `success`: Whether call succeeded

### Incident
- `cpu_usage`: CPU at incident time
- `threshold`: Threshold value
- `action`: Action taken (AUTOMATIC ROLLBACK)
- `ai_diagnosis`: AI analysis result (truncated)

### Performance Metrics
- `uptime_seconds`: System uptime
- `total_checks`: Number of monitoring checks
- `threshold_breaches`: Number of breaches
- `breach_rate`: Percentage of checks that breached
- `ai_calls`: Number of AI calls made
- `ai_failures`: Number of failed AI calls
- `ai_success_rate`: AI call success rate
- `avg_ai_duration_ms`: Average AI call duration

## Usage Examples

### Structured Logging
```python
from src.reporting.logger import log_with_context

log_with_context(
    logger,
    'warning',
    'High CPU detected',
    cpu=95.5,
    threshold=80.0,
    server='prod-01'
)
```

### Performance Tracking
```python
from src.reporting.metrics import PerformanceMetrics, Timer

metrics = PerformanceMetrics()
metrics.record_check()

with Timer() as timer:
    result = ai_provider.analyze(prompt)
    
metrics.record_ai_call(timer.duration_ms, success=True)
summary = metrics.get_summary()
```

## Integration with Log Aggregation

The structured format makes it easy to integrate with:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Splunk**
- **Datadog**
- **CloudWatch Logs Insights**

Example query (CloudWatch):
```
fields @timestamp, cpu_usage, threshold, breach_percentage
| filter @message like /THRESHOLD BREACHED/
| sort @timestamp desc
```

## Console vs File Logging

- **File**: All logs (INFO and above)
- **Console**: Only WARNING and above
- Both use structured formatting

## Next Steps

Completed refactoring steps:
- ✅ Step 1: Architecture & Project Structure
- ✅ Step 2: Configuration Management
- ✅ Step 3: Data Models & Type Safety
- ⏭️ Step 4: Error Handling & Resilience (skipped)
- ✅ Step 5: Dependency Injection & Testability
- ✅ Step 6: Logging & Observability

Ready for:
- Step 7: Testing Strategy (expand test coverage)
- Step 8: Code Quality Improvements
