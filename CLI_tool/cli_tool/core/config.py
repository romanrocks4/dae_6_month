"""
Core configuration management.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml

class Config:
    """Configuration manager for pentestctl."""
    
    def __init__(self, config_path: Optional[str] = None):
        # Always use the CLI tool's directory
        cli_tool_dir = Path(__file__).parent.parent.parent  # Go up three levels to get to the CLI tool root
        self.config_path = Path(config_path) if config_path else cli_tool_dir / "CLI-TOOL" / "config.yaml"
        self._config: Dict[str, Any] = {}
        self.load()
    
    def load(self):
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f) or {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation."""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)