"""
Helper utilities.
"""

import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

def get_trading_days(start_date, end_date):
    """
    Get list of trading days between dates.

    Parameters:
    -----------
    start_date : str or datetime
        Start date
    end_date : str or datetime
        End date

    Returns:
    --------
    pd.DatetimeIndex: Trading days
    """
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    return dates

def save_results(results, filepath, format='pickle'):
    """
    Save results to file.

    Parameters:
    -----------
    results : any
        Results to save
    filepath : str
        Output filepath
    format : str
        Format: 'pickle', 'csv', or 'json'
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    if format == 'pickle':
        with open(path, 'wb') as f:
            pickle.dump(results, f)
    elif format == 'csv':
        if isinstance(results, pd.DataFrame):
            results.to_csv(path)
        else:
            raise ValueError("CSV format requires pandas DataFrame")
    elif format == 'json':
        with open(path, 'w') as f:
            json.dump(results, f, indent=2)
    else:
        raise ValueError(f"Unknown format: {format}")

def load_results(filepath, format='pickle'):
    """
    Load results from file.

    Parameters:
    -----------
    filepath : str
        Input filepath
    format : str
        Format: 'pickle', 'csv', or 'json'

    Returns:
    --------
    any: Loaded results
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    if format == 'pickle':
        with open(path, 'rb') as f:
            return pickle.load(f)
    elif format == 'csv':
        return pd.read_csv(path, index_col=0, parse_dates=True)
    elif format == 'json':
        with open(path, 'r') as f:
            return json.load(f)
    else:
        raise ValueError(f"Unknown format: {format}")

def create_directory_structure():
    """Create necessary project directories if they don't exist."""
    directories = [
        'data/raw',
        'data/processed',
        'data/features',
        'data/results',
        'results/models',
        'results/plots',
        'results/reports',
    ]

    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def format_percentage(value, decimals=2):
    """
    Format value as percentage string.

    Parameters:
    -----------
    value : float
        Value to format
    decimals : int
        Number of decimal places

    Returns:
    --------
    str: Formatted percentage
    """
    return f"{value * 100:.{decimals}f}%"

def calculate_annualized_return(returns):
    """
    Calculate annualized return from a returns series.

    Parameters:
    -----------
    returns : pd.Series
        Daily returns

    Returns:
    --------
    float: Annualized return
    """
    total_return = (1 + returns).prod() - 1
    n_days = len(returns)
    n_years = n_days / 252
    annualized = (1 + total_return) ** (1 / n_years) - 1
    return annualized

def downsample_data(df, freq='W'):
    """
    Downsample time series data to lower frequency.

    Parameters:
    -----------
    df : pd.DataFrame
        Data with datetime index
    freq : str
        Frequency: 'W' (weekly), 'M' (monthly), etc.

    Returns:
    --------
    pd.DataFrame: Downsampled data
    """
    return df.resample(freq).last()

def print_summary_stats(df, title="Summary Statistics"):
    """
    Print summary statistics for a dataframe.

    Parameters:
    -----------
    df : pd.DataFrame
        Data to summarize
    title : str
        Title for the summary
    """
    print(f"\n{'=' * 60}")
    print(f"{title:^60}")
    print('=' * 60)
    print(df.describe())
    print('=' * 60)

def timer(func):
    """
    Decorator to time function execution.

    Usage:
    ------
    @timer
    def my_function():
        pass
    """
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

def chunk_list(lst, chunk_size):
    """
    Split a list into chunks.

    Parameters:
    -----------
    lst : list
        List to chunk
    chunk_size : int
        Size of each chunk

    Returns:
    --------
    list: List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
