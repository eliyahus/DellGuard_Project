"""Configuration management for DellGuard"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path to project root (3 levels up from this file)
    """
    return Path(__file__).parent.parent.parent


class Config:
    """Configuration loader and manager"""
    
    def __init__(self, config_path: Optional[str] = None) -> None:
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to config file. If None, uses default.yaml
        """
        if config_path is None:
            # Default to config/default.yaml
            project_root = get_project_root()
            config_path = str(project_root / "config" / "default.yaml")
        
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = self._load_config()
        self._apply_env_overrides()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load YAML configuration file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides"""
        # Example: DELLGUARD_AI_MODEL overrides ai.model
        env_mappings = {
            'DELLGUARD_AI_MODEL': ('ai', 'model'),
            'DELLGUARD_AI_PROVIDER': ('ai', 'provider'),
            'DELLGUARD_THRESHOLD_SIGMA': ('monitoring', 'threshold_sigma'),
            'DELLGUARD_LOG_LEVEL': ('logging', 'level'),
            'DELLGUARD_METRICS_FILE': ('data', 'metrics_file'),
        }
        
        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert to appropriate type
                if key == 'threshold_sigma':
                    self._config[section][key] = float(value)
                else:
                    self._config[section][key] = value
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(section, {}).get(key, default)
    
    @property
    def monitoring(self) -> Dict[str, Any]:
        """Get monitoring configuration"""
        return self._config.get('monitoring', {})
    
    @property
    def ai(self) -> Dict[str, Any]:
        """Get AI configuration"""
        return self._config.get('ai', {})
    
    @property
    def data(self) -> Dict[str, Any]:
        """Get data configuration"""
        return self._config.get('data', {})
    
    @property
    def logging(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self._config.get('logging', {})
    
    @property
    def visualization(self) -> Dict[str, Any]:
        """Get visualization configuration"""
        return self._config.get('visualization', {})


# Global config instance
_config_instance: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get or create global config instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance


def reload_config(config_path: Optional[str] = None) -> Config:
    """Reload configuration"""
    global _config_instance
    _config_instance = Config(config_path)
    return _config_instance
