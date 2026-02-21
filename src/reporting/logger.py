"""Structured logging configuration for DellGuard"""

import logging
import sys
from typing import Any, Dict
from pathlib import Path


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with structured data"""
        # Base message
        message = super().format(record)
        
        # Add structured data if present
        if hasattr(record, 'structured_data'):
            data = record.structured_data
            structured = ' | '.join([f"{k}={v}" for k, v in data.items()])
            message = f"{message} | {structured}"
        
        return message


def setup_logging(
    log_file: str = "incidents.log",
    log_level: str = "INFO",
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
) -> logging.Logger:
    """
    Setup structured logging for DellGuard.
    
    Args:
        log_file: Path to log file
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log message format
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("dellguard")
    logger.setLevel(getattr(logging, log_level))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # File handler with structured formatter
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level))
    file_handler.setFormatter(StructuredFormatter(log_format))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)  # Only warnings and above to console
    console_handler.setFormatter(StructuredFormatter(log_format))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def log_with_context(logger: logging.Logger, level: str, message: str, **kwargs: Any) -> None:
    """
    Log message with structured context data.
    
    Args:
        logger: Logger instance
        level: Log level (debug, info, warning, error, critical)
        message: Log message
        **kwargs: Structured data to include
    """
    log_func = getattr(logger, level.lower())
    
    # Create log record with structured data
    extra = {'structured_data': kwargs}
    log_func(message, extra=extra)


def log_threshold_breach(
    logger: logging.Logger,
    cpu_usage: float,
    threshold: float,
    breach_percentage: float
) -> None:
    """Log threshold breach with structured data"""
    log_with_context(
        logger,
        'warning',
        'THRESHOLD BREACHED',
        cpu_usage=f"{cpu_usage:.2f}%",
        threshold=f"{threshold:.2f}%",
        breach_percentage=f"{breach_percentage:.1f}%",
        severity='high'
    )


def log_system_start(logger: logging.Logger, threshold: float, sigma: float) -> None:
    """Log system startup with configuration"""
    log_with_context(
        logger,
        'info',
        'Guard system initialized',
        threshold=f"{threshold:.2f}%",
        sigma=sigma,
        status='active'
    )


def log_ai_analysis(logger: logging.Logger, duration_ms: float, success: bool) -> None:
    """Log AI analysis performance"""
    log_with_context(
        logger,
        'info',
        'AI analysis completed',
        duration_ms=f"{duration_ms:.2f}",
        success=success
    )


def log_incident(
    logger: logging.Logger,
    cpu_usage: float,
    threshold: float,
    ai_diagnosis: str,
    action: str
) -> None:
    """Log incident with full context"""
    log_with_context(
        logger,
        'error',
        'INCIDENT DETECTED - Automatic rollback initiated',
        cpu_usage=f"{cpu_usage:.2f}%",
        threshold=f"{threshold:.2f}%",
        action=action,
        ai_diagnosis=ai_diagnosis[:100]  # Truncate for log
    )
