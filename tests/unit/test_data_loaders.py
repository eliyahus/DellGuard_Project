"""Unit tests for data loaders"""

import pytest
from pathlib import Path
from src.data.loader import DataLoader, CSVDataLoader, MockDataLoader
from tests.constants import (
    TEST_BASELINE_MEAN,
    TEST_BASELINE_STD,
    TEST_BASELINE_MEAN_ALT,
    TEST_BASELINE_STD_ALT,
    TEST_BASELINE_MEAN_ALT2,
    TEST_BASELINE_STD_ALT2
)


def test_mock_data_loader_default_values() -> None:
    """Test MockDataLoader with default values"""
    loader = MockDataLoader()
    mean, std = loader.load_baseline_data()
    
    assert mean == TEST_BASELINE_MEAN
    assert std == TEST_BASELINE_STD


def test_mock_data_loader_custom_values() -> None:
    """Test MockDataLoader with custom values"""
    loader = MockDataLoader(mean=TEST_BASELINE_MEAN_ALT, std=TEST_BASELINE_STD_ALT)
    mean, std = loader.load_baseline_data()
    
    assert mean == TEST_BASELINE_MEAN_ALT
    assert std == TEST_BASELINE_STD_ALT


def test_mock_data_loader_consistent_results() -> None:
    """Test MockDataLoader returns consistent results"""
    loader = MockDataLoader(mean=TEST_BASELINE_MEAN_ALT2, std=TEST_BASELINE_STD_ALT2)
    
    mean1, std1 = loader.load_baseline_data()
    mean2, std2 = loader.load_baseline_data()
    
    assert mean1 == mean2 == TEST_BASELINE_MEAN_ALT2
    assert std1 == std2 == TEST_BASELINE_STD_ALT2


def test_csv_data_loader_initialization() -> None:
    """Test CSVDataLoader initialization"""
    file_path = Path("test.csv")
    loader = CSVDataLoader(file_path=file_path, baseline_status="Normal")
    
    assert loader.file_path == file_path
    assert loader.baseline_status == "Normal"


def test_csv_data_loader_default_status() -> None:
    """Test CSVDataLoader uses default baseline status"""
    file_path = Path("test.csv")
    loader = CSVDataLoader(file_path=file_path)
    
    assert loader.baseline_status == "Normal"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
