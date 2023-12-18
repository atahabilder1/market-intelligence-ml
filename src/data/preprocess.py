"""Data preprocessing utilities."""

import pandas as pd
import numpy as np

def calculate_returns(prices, periods=[1, 5, 20]):
    """Calculate returns for multiple periods."""
    returns = {}
    for period in periods:
        returns[f'return_{period}d'] = prices.pct_change(period)
    return pd.DataFrame(returns)

def clean_data(df):
    """Clean data: handle missing values."""
    df = df.dropna()
    return df
