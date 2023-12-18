"""Technical indicator calculations."""

import pandas as pd
import numpy as np

def calculate_rsi(prices, period=14):
    """Calculate RSI."""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_moving_averages(prices, windows=[5, 10, 20, 50, 200]):
    """Calculate multiple MAs."""
    mas = {}
    for window in windows:
        mas[f'ma_{window}'] = prices.rolling(window=window).mean()
    return pd.DataFrame(mas)
