"""Unit tests for data models"""

import pytest
from datetime import datetime
from src.data.models import ServerMetrics, ThresholdConfig, IncidentReport


def test_server_metrics_creation():
    """Test ServerMetrics dataclass creation"""
    metrics = ServerMetrics(
        timestamp=1234567890.0,
        cpu_usage=45.5,
        latency_ms=120.0,
        error_rate=0.02,
        status="Normal"
    )
    
    assert metrics.cpu_usage == 45.5
    assert metrics.status == "Normal"
    assert metrics.is_critical() is False


def test_server_metrics_critical():
    """Test critical status detection"""
    metrics = ServerMetrics(
        timestamp=1234567890.0,
        cpu_usage=98.5,
        latency_ms=500.0,
        error_rate=0.15,
        status="CRITICAL"
    )
    
    assert metrics.is_critical() is True


def test_threshold_config_breach():
    """Test threshold breach detection"""
    threshold = ThresholdConfig(cpu_threshold=50.0, sigma=3.0)
    
    assert threshold.is_breached(60.0) is True
    assert threshold.is_breached(50.1) is True
    assert threshold.is_breached(50.0) is False
    assert threshold.is_breached(40.0) is False


def test_incident_report_breach_percentage():
    """Test breach percentage calculation"""
    incident = IncidentReport(
        timestamp=datetime.now(),
        cpu_usage=75.0,
        threshold=50.0,
        ai_diagnosis="Test diagnosis",
        action_taken="ROLLBACK"
    )
    
    # (75 - 50) / 50 * 100 = 50%
    assert incident.breach_percentage() == 50.0


def test_incident_report_with_optional_diagnosis():
    """Test incident report with no AI diagnosis"""
    incident = IncidentReport(
        timestamp=datetime.now(),
        cpu_usage=60.0,
        threshold=50.0,
        ai_diagnosis=None,
        action_taken="ROLLBACK"
    )
    
    assert incident.ai_diagnosis is None
    assert incident.action_taken == "ROLLBACK"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
