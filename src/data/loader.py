"""Data loader abstraction"""

from abc import ABC, abstractmethod
import pandas as pd
from pathlib import Path
from typing import Tuple


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
        df = pd.read_csv(self.file_path)
        healthy_data = df[df['Status'] == self.baseline_status]
        
        mean_cpu: float = healthy_data['CPU_Usage'].mean()
        std_cpu: float = healthy_data['CPU_Usage'].std()
        
        return mean_cpu, std_cpu


class MockDataLoader(DataLoader):
    """Mock data loader for testing"""
    
    def __init__(self, mean: float = 40.0, std: float = 5.0) -> None:
        self.mean = mean
        self.std = std
    
    def load_baseline_data(self) -> Tuple[float, float]:
        """Return mock baseline data"""
        return self.mean, self.std
