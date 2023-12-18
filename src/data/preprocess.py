"""Data preprocessing utilities."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

def calculate_returns(prices, periods=[1, 5, 20]):
    """Calculate returns for multiple periods."""
    returns = {}
    for period in periods:
        returns[f'return_{period}d'] = prices.pct_change(period)
    return pd.DataFrame(returns)

def clean_data(df):
    """Clean data: handle missing values, outliers, and duplicates."""
    # Remove duplicates
    df = df[~df.index.duplicated(keep='first')]

    # Forward fill then backward fill for missing values
    df = df.fillna(method='ffill').fillna(method='bfill')

    # Drop any remaining NaN values
    df = df.dropna()

    return df

def normalize_data(df, method='zscore'):
    """
    Normalize data using various methods.

    Parameters:
    -----------
    df : pd.DataFrame
        Data to normalize
    method : str
        Normalization method: 'zscore', 'minmax', or 'robust'

    Returns:
    --------
    pd.DataFrame: Normalized data
    """
    if method == 'zscore':
        return (df - df.mean()) / df.std()
    elif method == 'minmax':
        return (df - df.min()) / (df.max() - df.min())
    elif method == 'robust':
        median = df.median()
        q75, q25 = df.quantile(0.75), df.quantile(0.25)
        iqr = q75 - q25
        return (df - median) / iqr
    else:
        raise ValueError(f"Unknown normalization method: {method}")

def create_lagged_features(df, columns, lags=[1, 2, 3, 5]):
    """
    Create lagged features for time series prediction.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : list
        Columns to create lags for
    lags : list
        Number of periods to lag

    Returns:
    --------
    pd.DataFrame: DataFrame with lagged features
    """
    lagged_df = df.copy()

    for col in columns:
        if col in df.columns:
            for lag in lags:
                lagged_df[f'{col}_lag_{lag}'] = df[col].shift(lag)

    return lagged_df

def split_train_val_test(df, train_end, val_end):
    """
    Split time series data into train, validation, and test sets.

    Parameters:
    -----------
    df : pd.DataFrame
        Time series dataframe with datetime index
    train_end : str
        End date for training set (e.g., '2023-12-31')
    val_end : str
        End date for validation set (e.g., '2024-06-30')

    Returns:
    --------
    tuple: (train_df, val_df, test_df)
    """
    train = df[df.index <= train_end]
    val = df[(df.index > train_end) & (df.index <= val_end)]
    test = df[df.index > val_end]

    return train, val, test

def handle_outliers(df, columns=None, method='iqr', threshold=3.0):
    """
    Handle outliers in the data.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : list, optional
        Columns to check for outliers (default: all numeric columns)
    method : str
        Method to detect outliers: 'iqr' or 'zscore'
    threshold : float
        Threshold for outlier detection

    Returns:
    --------
    pd.DataFrame: DataFrame with outliers handled
    """
    df_clean = df.copy()

    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns

    for col in columns:
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR

            # Cap outliers
            df_clean[col] = df[col].clip(lower_bound, upper_bound)

        elif method == 'zscore':
            mean = df[col].mean()
            std = df[col].std()
            lower_bound = mean - threshold * std
            upper_bound = mean + threshold * std

            # Cap outliers
            df_clean[col] = df[col].clip(lower_bound, upper_bound)

    return df_clean

def align_datasets(datasets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Align multiple datasets to have the same date range.

    Parameters:
    -----------
    datasets : dict
        Dictionary of dataframes with datetime index

    Returns:
    --------
    dict: Dictionary of aligned dataframes
    """
    # Find common date range
    start_date = max([df.index.min() for df in datasets.values()])
    end_date = min([df.index.max() for df in datasets.values()])

    # Align all datasets
    aligned = {}
    for name, df in datasets.items():
        aligned[name] = df[(df.index >= start_date) & (df.index <= end_date)]

    return aligned
