import pandas as pd
from pathlib import Path
from typing import Optional
from src.utils.config import get_config, get_project_root
from src.utils.exceptions import ThresholdCalculationError


def calculate_baseline_threshold() -> Optional[float]:
    """
    Calculate CPU threshold based on baseline data using 3-sigma rule.
    
    The 3-sigma rule states that 99.7% of data falls within 3 standard deviations
    of the mean. We use this to set a threshold that catches true anomalies while
    minimizing false positives.
    
    Returns:
        CPU threshold value or None if calculation fails
    """
    config = get_config()
    
    # Get project root and construct file path
    project_root = get_project_root()
    file_path = project_root / config.get('data', 'metrics_file')
    
    print(f"Looking for data in: {file_path}")

    if not file_path.exists():
        raise ThresholdCalculationError(f"Data file not found: {file_path}")

    try:
        metrics_df = pd.read_csv(file_path)
        
        # Filter: learn only from healthy data to establish baseline
        baseline_status: str = config.get('data', 'baseline_status')
        healthy_data = metrics_df[metrics_df['Status'] == baseline_status]
        
        if healthy_data.empty:
            raise ThresholdCalculationError(f"No baseline data with status '{baseline_status}'")
        
        # Calculate statistical baseline from healthy server behavior
        avg_cpu: float = healthy_data['CPU_Usage'].mean()
        std_cpu: float = healthy_data['CPU_Usage'].std()
        
        if pd.isna(avg_cpu) or pd.isna(std_cpu):
            raise ThresholdCalculationError("Invalid baseline: contains NaN values")
        
        # Apply N-sigma threshold (default: 3-sigma for 99.7% confidence)
        sigma: float = config.get('monitoring', 'threshold_sigma')
        cpu_threshold: float = avg_cpu + (sigma * std_cpu)
        
        print("\n--- BASELINE CALCULATED ---")
        print(f"Average CPU: {avg_cpu:.2f}%")
        print(f"Critical Threshold ({sigma}-Sigma): {cpu_threshold:.2f}%")
        
        return cpu_threshold
    except pd.errors.EmptyDataError:
        raise ThresholdCalculationError("Data file is empty")
    except KeyError as e:
        raise ThresholdCalculationError(f"Missing required column: {e}")
    except Exception as e:
        raise ThresholdCalculationError(f"Threshold calculation failed: {e}")

if __name__ == "__main__":
    calculate_baseline_threshold()