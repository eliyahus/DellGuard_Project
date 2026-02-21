"""Unit tests for configuration management"""

import pytest
import os
from pathlib import Path
from src.utils.config import Config


def test_config_loads_default_yaml(tmp_path):
    """Test Config loads default.yaml"""
    # Create a temporary config file
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text("""
monitoring:
  threshold_sigma: 3
  check_interval_seconds: 5

ai:
  provider: ollama
  model: llama3

data:
  metrics_file: server_metrics.csv
  baseline_status: Normal

logging:
  level: INFO
  file: incidents.log
  format: "%(asctime)s - %(levelname)s - %(message)s"

visualization:
  output_file: chart.png
  figure_size: [12, 6]
  dpi: 100
""")
    
    config = Config(str(config_file))
    
    assert config.get('monitoring', 'threshold_sigma') == 3
    assert config.get('ai', 'model') == 'llama3'
    assert config.get('data', 'baseline_status') == 'Normal'


def test_config_get_with_default():
    """Test Config.get() with default value"""
    config_file = Path(__file__).parent.parent.parent / "config" / "default.yaml"
    config = Config(str(config_file))
    
    # Non-existent key should return default
    result = config.get('nonexistent', 'key', default='default_value')
    assert result == 'default_value'


def test_config_properties():
    """Test Config property accessors"""
    config_file = Path(__file__).parent.parent.parent / "config" / "default.yaml"
    config = Config(str(config_file))
    
    assert isinstance(config.monitoring, dict)
    assert isinstance(config.ai, dict)
    assert isinstance(config.data, dict)
    assert isinstance(config.logging, dict)
    assert isinstance(config.visualization, dict)


def test_config_env_override(tmp_path, monkeypatch):
    """Test environment variable overrides"""
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text("""
ai:
  model: llama3
  provider: ollama

monitoring:
  threshold_sigma: 3
""")
    
    # Set environment variables
    monkeypatch.setenv('DELLGUARD_AI_MODEL', 'llama3.1')
    monkeypatch.setenv('DELLGUARD_THRESHOLD_SIGMA', '4.0')
    
    config = Config(str(config_file))
    
    assert config.get('ai', 'model') == 'llama3.1'
    assert config.get('monitoring', 'threshold_sigma') == 4.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
