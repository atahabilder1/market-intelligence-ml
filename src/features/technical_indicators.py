"""Technical indicator calculations."""

import pandas as pd
import numpy as np

def calculate_rsi(prices, period=14):
    """
    Calculate Relative Strength Index.

    Parameters:
    -----------
    prices : pd.Series
        Price series
    period : int
        RSI period (default: 14)

    Returns:
    --------
    pd.Series: RSI values
    """
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_moving_averages(prices, windows=[5, 10, 20, 50, 200]):
    """
    Calculate multiple Simple Moving Averages.

    Parameters:
    -----------
    prices : pd.Series
        Price series
    windows : list
        List of window sizes

    Returns:
    --------
    pd.DataFrame: DataFrame with MA columns
    """
    mas = {}
    for window in windows:
        mas[f'ma_{window}'] = prices.rolling(window=window).mean()
    return pd.DataFrame(mas)

def calculate_ema(prices, span=20):
    """
    Calculate Exponential Moving Average.

    Parameters:
    -----------
    prices : pd.Series
        Price series
    span : int
        EMA span

    Returns:
    --------
    pd.Series: EMA values
    """
    return prices.ewm(span=span, adjust=False).mean()

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """
    Calculate MACD (Moving Average Convergence Divergence).

    Parameters:
    -----------
    prices : pd.Series
        Price series
    fast : int
        Fast EMA period
    slow : int
        Slow EMA period
    signal : int
        Signal line period

    Returns:
    --------
    pd.DataFrame: MACD, signal, and histogram
    """
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return pd.DataFrame({
        'macd': macd_line,
        'macd_signal': signal_line,
        'macd_hist': histogram
    })

def calculate_bollinger_bands(prices, window=20, num_std=2):
    """
    Calculate Bollinger Bands.

    Parameters:
    -----------
    prices : pd.Series
        Price series
    window : int
        Moving average window
    num_std : int
        Number of standard deviations

    Returns:
    --------
    pd.DataFrame: Upper band, middle band, lower band
    """
    middle_band = prices.rolling(window=window).mean()
    std = prices.rolling(window=window).std()

    upper_band = middle_band + (std * num_std)
    lower_band = middle_band - (std * num_std)

    return pd.DataFrame({
        'bb_upper': upper_band,
        'bb_middle': middle_band,
        'bb_lower': lower_band,
        'bb_width': upper_band - lower_band
    })

def calculate_atr(high, low, close, period=14):
    """
    Calculate Average True Range.

    Parameters:
    -----------
    high : pd.Series
        High prices
    low : pd.Series
        Low prices
    close : pd.Series
        Close prices
    period : int
        ATR period

    Returns:
    --------
    pd.Series: ATR values
    """
    high_low = high - low
    high_close = np.abs(high - close.shift())
    low_close = np.abs(low - close.shift())

    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()

    return atr

def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    """
    Calculate Stochastic Oscillator.

    Parameters:
    -----------
    high : pd.Series
        High prices
    low : pd.Series
        Low prices
    close : pd.Series
        Close prices
    k_period : int
        %K period
    d_period : int
        %D period

    Returns:
    --------
    pd.DataFrame: %K and %D values
    """
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()

    k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d = k.rolling(window=d_period).mean()

    return pd.DataFrame({
        'stoch_k': k,
        'stoch_d': d
    })

def calculate_adx(high, low, close, period=14):
    """
    Calculate Average Directional Index.

    Parameters:
    -----------
    high : pd.Series
        High prices
    low : pd.Series
        Low prices
    close : pd.Series
        Close prices
    period : int
        ADX period

    Returns:
    --------
    pd.Series: ADX values
    """
    # Calculate +DM and -DM
    high_diff = high.diff()
    low_diff = -low.diff()

    pos_dm = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0)
    neg_dm = low_diff.where((low_diff > high_diff) & (low_diff > 0), 0)

    # Calculate ATR
    atr = calculate_atr(high, low, close, period)

    # Calculate +DI and -DI
    pos_di = 100 * (pos_dm.rolling(window=period).mean() / atr)
    neg_di = 100 * (neg_dm.rolling(window=period).mean() / atr)

    # Calculate DX and ADX
    dx = 100 * np.abs(pos_di - neg_di) / (pos_di + neg_di)
    adx = dx.rolling(window=period).mean()

    return adx

def calculate_obv(close, volume):
    """
    Calculate On-Balance Volume.

    Parameters:
    -----------
    close : pd.Series
        Close prices
    volume : pd.Series
        Volume data

    Returns:
    --------
    pd.Series: OBV values
    """
    obv = (np.sign(close.diff()) * volume).fillna(0).cumsum()
    return obv

def calculate_momentum(prices, period=10):
    """
    Calculate price momentum.

    Parameters:
    -----------
    prices : pd.Series
        Price series
    period : int
        Momentum period

    Returns:
    --------
    pd.Series: Momentum values
    """
    return prices.diff(period)

def calculate_roc(prices, period=12):
    """
    Calculate Rate of Change.

    Parameters:
    -----------
    prices : pd.Series
        Price series
    period : int
        ROC period

    Returns:
    --------
    pd.Series: ROC values
    """
    return ((prices - prices.shift(period)) / prices.shift(period)) * 100

def calculate_all_indicators(df, price_col='Close'):
    """
    Calculate all technical indicators for a price dataframe.

    Parameters:
    -----------
    df : pd.DataFrame
        OHLCV dataframe
    price_col : str
        Column name for close price

    Returns:
    --------
    pd.DataFrame: DataFrame with all indicators
    """
    indicators = pd.DataFrame(index=df.index)

    # Price
    close = df[price_col] if price_col in df.columns else df['Close']

    # Moving Averages
    ma_df = calculate_moving_averages(close)
    indicators = pd.concat([indicators, ma_df], axis=1)

    # EMA
    for span in [12, 26, 50]:
        indicators[f'ema_{span}'] = calculate_ema(close, span)

    # RSI
    indicators['rsi'] = calculate_rsi(close)

    # MACD
    macd_df = calculate_macd(close)
    indicators = pd.concat([indicators, macd_df], axis=1)

    # Bollinger Bands
    bb_df = calculate_bollinger_bands(close)
    indicators = pd.concat([indicators, bb_df], axis=1)

    # Momentum and ROC
    indicators['momentum'] = calculate_momentum(close)
    indicators['roc'] = calculate_roc(close)

    # If OHLCV data is available
    if all(col in df.columns for col in ['High', 'Low', 'Close']):
        indicators['atr'] = calculate_atr(df['High'], df['Low'], df['Close'])
        stoch_df = calculate_stochastic(df['High'], df['Low'], df['Close'])
        indicators = pd.concat([indicators, stoch_df], axis=1)
        indicators['adx'] = calculate_adx(df['High'], df['Low'], df['Close'])

    if 'Volume' in df.columns:
        indicators['obv'] = calculate_obv(close, df['Volume'])

    return indicators
