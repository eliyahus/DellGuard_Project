"""Custom exceptions for DellGuard system"""


class DellGuardException(Exception):
    """Base exception for all DellGuard errors"""
    pass


class DataLoadError(DellGuardException):
    """Raised when data loading fails"""
    pass


class AIProviderError(DellGuardException):
    """Raised when AI provider operations fail"""
    pass


class ThresholdCalculationError(DellGuardException):
    """Raised when threshold calculation fails"""
    pass


class MonitoringError(DellGuardException):
    """Raised when monitoring workflow fails"""
    pass
