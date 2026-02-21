"""Data loader abstraction"""

from abc import ABC, abstractmethod
import pandas as pd
from pathlib import Path
from typing import Tuple
from src.utils.exceptions import DataLoadError


class DataLoader(ABC):
    """Abstract base class for data loading"""
    
    @abstractmethod
    def load_baseline_data(self) -> Tuple[float, float]:
        """
        Load baseline data and calculate statistics.
        
        Returns:
            Tuple of (mean, std) for CPU usage
        """
        pass


class CSVDataLoader(DataLoader):
    """CSV file data loader"""
    
    def __init__(self, file_path: Path, baseline_status: str = "Normal") -> None:
        self.file_path = file_path
        self.baseline_status = baseline_status
    
    def load_baseline_data(self) -> Tuple[float, float]:
        """Load baseline from CSV file"""
        try:
            df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            raise DataLoadError(f"Data file not found: {self.file_path}")
        except pd.errors.EmptyDataError:
            raise DataLoadError(f"Data file is empty: {self.file_path}")
        except Exception as e:
            raise DataLoadError(f"Failed to read data file: {e}")
        
        healthy_data = df[df['Status'] == self.baseline_status]
        
        if healthy_data.empty:
            raise DataLoadError(f"No data found with status '{self.baseline_status}'")
        
        if 'CPU_Usage' not in df.columns:
            raise DataLoadError("CSV file missing 'CPU_Usage' column")
        
        mean_cpu: float = healthy_data['CPU_Usage'].mean()
        std_cpu: float = healthy_data['CPU_Usage'].std()
        
        if pd.isna(mean_cpu) or pd.isna(std_cpu):
            raise DataLoadError("Invalid baseline data: contains NaN values")
        
        return mean_cpu, std_cpu


class MockDataLoader(DataLoader):
    """Mock data loader for testing"""
    
    def __init__(self, mean: float = 40.0, std: float = 5.0) -> None:
        self.mean = mean
        self.std = std
    
    def load_baseline_data(self) -> Tuple[float, float]:
        """Return mock baseline data"""
        return self.mean, self.std
