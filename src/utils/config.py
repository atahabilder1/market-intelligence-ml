"""
Configuration management.
"""

import yaml
from pathlib import Path
from typing import Dict, Any

def load_config(config_path='configs/config.yaml'):
    """
    Load configuration from YAML file.

    Parameters:
    -----------
    config_path : str
        Path to config file

    Returns:
    --------
    dict: Configuration dictionary
    """
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    return config

def get_asset_list(config: Dict[str, Any]) -> list:
    """
    Extract complete asset list from config.

    Parameters:
    -----------
    config : dict
        Configuration dictionary

    Returns:
    --------
    list: List of all asset tickers
    """
    assets = []

    if 'assets' in config:
        for category in ['equities', 'fixed_income', 'alternatives', 'crypto', 'macro']:
            if category in config['assets']:
                assets.extend(config['assets'][category])

    return assets

def get_date_range(config: Dict[str, Any]) -> tuple:
    """
    Extract date range from config.

    Parameters:
    -----------
    config : dict
        Configuration dictionary

    Returns:
    --------
    tuple: (start_date, end_date, train_end, val_end)
    """
    if 'data' not in config:
        raise ValueError("'data' section missing from config")

    return (
        config['data'].get('start_date'),
        config['data'].get('end_date'),
        config['data'].get('train_end'),
        config['data'].get('val_end')
    )

def get_model_params(config: Dict[str, Any], model_name: str) -> Dict[str, Any]:
    """
    Get parameters for a specific model.

    Parameters:
    -----------
    config : dict
        Configuration dictionary
    model_name : str
        Name of the model

    Returns:
    --------
    dict: Model parameters
    """
    if 'models' not in config or model_name not in config['models']:
        return {}

    return config['models'][model_name]

def get_feature_params(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get feature engineering parameters.

    Parameters:
    -----------
    config : dict
        Configuration dictionary

    Returns:
    --------
    dict: Feature parameters
    """
    return config.get('features', {})
