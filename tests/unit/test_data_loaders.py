"""Unit tests for data loaders"""

import pytest
from pathlib import Path
from src.data.loader import DataLoader, CSVDataLoader, MockDataLoader


def test_mock_data_loader_default_values():
    """Test MockDataLoader with default values"""
    loader = MockDataLoader()
    mean, std = loader.load_baseline_data()
    
    assert mean == 40.0
    assert std == 5.0


def test_mock_data_loader_custom_values():
    """Test MockDataLoader with custom values"""
    loader = MockDataLoader(mean=50.0, std=10.0)
    mean, std = loader.load_baseline_data()
    
    assert mean == 50.0
    assert std == 10.0


def test_mock_data_loader_consistent_results():
    """Test MockDataLoader returns consistent results"""
    loader = MockDataLoader(mean=45.0, std=7.5)
    
    mean1, std1 = loader.load_baseline_data()
    mean2, std2 = loader.load_baseline_data()
    
    assert mean1 == mean2 == 45.0
    assert std1 == std2 == 7.5


def test_csv_data_loader_initialization():
    """Test CSVDataLoader initialization"""
    file_path = Path("test.csv")
    loader = CSVDataLoader(file_path=file_path, baseline_status="Normal")
    
    assert loader.file_path == file_path
    assert loader.baseline_status == "Normal"


def test_csv_data_loader_default_status():
    """Test CSVDataLoader uses default baseline status"""
    file_path = Path("test.csv")
    loader = CSVDataLoader(file_path=file_path)
    
    assert loader.baseline_status == "Normal"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
