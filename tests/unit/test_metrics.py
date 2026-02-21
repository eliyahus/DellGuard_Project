"""Unit tests for performance metrics"""

import pytest
from src.reporting.metrics import PerformanceMetrics, Timer
import time
from tests.constants import (
    TEST_AI_DURATION_FAST_MS,
    TEST_AI_DURATION_NORMAL_MS,
    TEST_AI_DURATION_SLOW_MS,
    TEST_SLEEP_DURATION_SECONDS
)


def test_performance_metrics_initialization() -> None:
    """Test PerformanceMetrics initializes with zeros"""
    metrics = PerformanceMetrics()
    
    assert metrics.total_checks == 0
    assert metrics.threshold_breaches == 0
    assert metrics.ai_calls == 0
    assert metrics.ai_failures == 0
    assert metrics.total_ai_duration_ms == 0.0


def test_performance_metrics_record_check() -> None:
    """Test recording monitoring checks"""
    metrics = PerformanceMetrics()
    
    metrics.record_check()
    metrics.record_check()
    metrics.record_check()
    
    assert metrics.total_checks == 3


def test_performance_metrics_record_breach() -> None:
    """Test recording threshold breaches"""
    metrics = PerformanceMetrics()
    
    metrics.record_breach()
    metrics.record_breach()
    
    assert metrics.threshold_breaches == 2


def test_performance_metrics_record_ai_call_success() -> None:
    """Test recording successful AI call"""
    metrics = PerformanceMetrics()
    
    metrics.record_ai_call(duration_ms=TEST_AI_DURATION_SLOW_MS, success=True)
    
    assert metrics.ai_calls == 1
    assert metrics.ai_failures == 0
    assert metrics.total_ai_duration_ms == TEST_AI_DURATION_SLOW_MS


def test_performance_metrics_record_ai_call_failure() -> None:
    """Test recording failed AI call"""
    metrics = PerformanceMetrics()
    
    metrics.record_ai_call(duration_ms=TEST_AI_DURATION_FAST_MS, success=False)
    
    assert metrics.ai_calls == 1
    assert metrics.ai_failures == 1
    assert metrics.total_ai_duration_ms == TEST_AI_DURATION_FAST_MS


def test_performance_metrics_summary() -> None:
    """Test metrics summary calculation"""
    metrics = PerformanceMetrics()
    
    # Simulate some activity
    for _ in range(10):
        metrics.record_check()
    
    metrics.record_breach()
    metrics.record_breach()
    
    metrics.record_ai_call(TEST_AI_DURATION_NORMAL_MS, success=True)
    metrics.record_ai_call(TEST_AI_DURATION_SLOW_MS, success=True)
    metrics.record_ai_call(TEST_AI_DURATION_FAST_MS, success=False)
    
    summary = metrics.get_summary()
    
    assert summary['total_checks'] == 10
    assert summary['threshold_breaches'] == 2
    assert summary['breach_rate'] == 0.2  # 2/10
    assert summary['ai_calls'] == 3
    assert summary['ai_failures'] == 1
    assert summary['ai_success_rate'] == pytest.approx(0.667, rel=0.01)
    # (1000 + 1500 + 500) / 3 = 1000
    assert summary['avg_ai_duration_ms'] == TEST_AI_DURATION_NORMAL_MS


def test_timer_context_manager() -> None:
    """Test Timer context manager"""
    with Timer() as timer:
        time.sleep(TEST_SLEEP_DURATION_SECONDS)
    
    # Should be at least 10ms (TEST_SLEEP_DURATION_SECONDS=0.01)
    assert timer.duration_ms >= TEST_SLEEP_DURATION_SECONDS * 1000
    assert timer.start is not None
    assert timer.end is not None


def test_timer_multiple_uses() -> None:
    """Test Timer can be used multiple times"""
    timer1 = Timer()
    with timer1:
        time.sleep(TEST_SLEEP_DURATION_SECONDS)
    
    timer2 = Timer()
    with timer2:
        time.sleep(TEST_SLEEP_DURATION_SECONDS * 2)
    
    assert timer1.duration_ms < timer2.duration_ms


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
