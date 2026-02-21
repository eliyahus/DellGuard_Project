"""Tests for error handling and exceptions"""

import pytest
from pathlib import Path
from src.utils.exceptions import (
    DellGuardException,
    DataLoadError,
    AIProviderError,
    ThresholdCalculationError,
    MonitoringError
)
from src.data.loader import CSVDataLoader
from src.ai.providers import OllamaProvider
from src.core.monitor import GuardSystem
from tests.constants import TEST_BASELINE_MEAN, TEST_BASELINE_STD, TEST_SIGMA


def test_data_load_error_file_not_found() -> None:
    """Test DataLoadError when file doesn't exist"""
    loader = CSVDataLoader(Path("nonexistent.csv"))
    
    with pytest.raises(DataLoadError, match="Data file not found"):
        loader.load_baseline_data()


def test_data_load_error_empty_file(tmp_path: Path) -> None:
    """Test DataLoadError with empty CSV"""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")
    
    loader = CSVDataLoader(empty_file)
    
    with pytest.raises(DataLoadError, match="Data file is empty"):
        loader.load_baseline_data()


def test_data_load_error_missing_column(tmp_path: Path) -> None:
    """Test DataLoadError when required column is missing"""
    csv_file = tmp_path / "bad_columns.csv"
    csv_file.write_text("Status,Value\nNormal,100\n")
    
    loader = CSVDataLoader(csv_file)
    
    with pytest.raises(DataLoadError, match="missing 'CPU_Usage' column"):
        loader.load_baseline_data()


def test_data_load_error_no_baseline_data(tmp_path: Path) -> None:
    """Test DataLoadError when no data matches baseline status"""
    csv_file = tmp_path / "no_baseline.csv"
    csv_file.write_text("Status,CPU_Usage\nCritical,100\n")
    
    loader = CSVDataLoader(csv_file, baseline_status="Normal")
    
    with pytest.raises(DataLoadError, match="No data found with status"):
        loader.load_baseline_data()


def test_threshold_calculation_error(mock_ai_provider, console_reporter) -> None:
    """Test ThresholdCalculationError when data loading fails"""
    from src.data.loader import CSVDataLoader
    
    bad_loader = CSVDataLoader(Path("nonexistent.csv"))
    
    guard = GuardSystem(
        data_loader=bad_loader,
        ai_provider=mock_ai_provider,
        reporter=console_reporter,
        sigma=TEST_SIGMA
    )
    
    with pytest.raises(ThresholdCalculationError):
        guard.calculate_threshold()


def test_ai_provider_error_inheritance() -> None:
    """Test exception hierarchy"""
    assert issubclass(AIProviderError, DellGuardException)
    assert issubclass(DataLoadError, DellGuardException)
    assert issubclass(ThresholdCalculationError, DellGuardException)
    assert issubclass(MonitoringError, DellGuardException)


def test_custom_exception_messages() -> None:
    """Test custom exception messages"""
    exc = DataLoadError("Test message")
    assert str(exc) == "Test message"
    
    exc2 = AIProviderError("AI failed")
    assert str(exc2) == "AI failed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
