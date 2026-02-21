"""Performance metrics and monitoring"""

import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PerformanceMetrics:
    """Track performance metrics for monitoring"""
    total_checks: int = 0
    threshold_breaches: int = 0
    ai_calls: int = 0
    ai_failures: int = 0
    total_ai_duration_ms: float = 0.0
    start_time: datetime = field(default_factory=datetime.now)
    
    def record_check(self) -> None:
        """Record a monitoring check"""
        self.total_checks += 1
    
    def record_breach(self) -> None:
        """Record a threshold breach"""
        self.threshold_breaches += 1
    
    def record_ai_call(self, duration_ms: float, success: bool = True) -> None:
        """Record an AI analysis call"""
        self.ai_calls += 1
        self.total_ai_duration_ms += duration_ms
        if not success:
            self.ai_failures += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        avg_ai_duration = (
            self.total_ai_duration_ms / self.ai_calls 
            if self.ai_calls > 0 else 0
        )
        
        return {
            'uptime_seconds': uptime,
            'total_checks': self.total_checks,
            'threshold_breaches': self.threshold_breaches,
            'breach_rate': (
                self.threshold_breaches / self.total_checks 
                if self.total_checks > 0 else 0
            ),
            'ai_calls': self.ai_calls,
            'ai_failures': self.ai_failures,
            'ai_success_rate': (
                (self.ai_calls - self.ai_failures) / self.ai_calls 
                if self.ai_calls > 0 else 0
            ),
            'avg_ai_duration_ms': avg_ai_duration
        }


class Timer:
    """Context manager for timing operations"""
    
    def __init__(self) -> None:
        self.start: Optional[float] = None
        self.end: Optional[float] = None
        self.duration_ms: float = 0.0
    
    def __enter__(self) -> 'Timer':
        self.start = time.time()
        return self
    
    def __exit__(self, *args: Any) -> None:
        self.end = time.time()
        if self.start:
            self.duration_ms = (self.end - self.start) * 1000
