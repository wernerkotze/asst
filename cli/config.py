"""
Configuration module for the ASST CLI.
"""

import os
from typing import Dict, Any

# Default configuration
DEFAULT_CONFIG = {
    "api_url": "http://localhost:8000",
    "output_format": "text",
    "timeout": 30,  # Request timeout in seconds
}

def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables.
    
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()
    
    # Override with environment variables
    if os.environ.get("ASST_API_URL"):
        config["api_url"] = os.environ.get("ASST_API_URL")
    
    if os.environ.get("ASST_OUTPUT_FORMAT"):
        config["output_format"] = os.environ.get("ASST_OUTPUT_FORMAT")
    
    if os.environ.get("ASST_TIMEOUT"):
        config["timeout"] = int(os.environ.get("ASST_TIMEOUT"))
    
    return config

def get_config_value(key: str, default: Any = None) -> Any:
    """
    Get a configuration value.
    
    Args:
        key: Configuration key
        default: Default value if key is not found
        
    Returns:
        Any: Configuration value
    """
    config = load_config()
    return config.get(key, default)
