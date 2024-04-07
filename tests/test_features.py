"""
Unit tests for feature engineering modules.
"""

import pytest
import numpy as np
import pandas as pd
from src.features.technical_indicators import (
    calculate_rsi, calculate_moving_averages, calculate_macd,
    calculate_bollinger_bands
)
from src.features.macro_features import vix_regime_features

@pytest.fixture
def sample_prices():
    """Create sample price data."""
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', periods=100)
    prices = pd.Series(100 + np.cumsum(np.random.randn(100) * 2), index=dates)
    return prices

def test_rsi_calculation(sample_prices):
    """Test RSI calculation."""
    rsi = calculate_rsi(sample_prices, period=14)

    assert isinstance(rsi, pd.Series)
    assert len(rsi) == len(sample_prices)
    # RSI should be between 0 and 100
    assert rsi.dropna().min() >= 0
    assert rsi.dropna().max() <= 100

def test_moving_averages(sample_prices):
    """Test moving average calculation."""
    mas = calculate_moving_averages(sample_prices, windows=[5, 10, 20])

    assert isinstance(mas, pd.DataFrame)
    assert 'ma_5' in mas.columns
    assert 'ma_10' in mas.columns
    assert 'ma_20' in mas.columns

def test_macd(sample_prices):
    """Test MACD calculation."""
    macd_df = calculate_macd(sample_prices)

    assert isinstance(macd_df, pd.DataFrame)
    assert 'macd' in macd_df.columns
    assert 'macd_signal' in macd_df.columns
    assert 'macd_hist' in macd_df.columns

def test_bollinger_bands(sample_prices):
    """Test Bollinger Bands calculation."""
    bb_df = calculate_bollinger_bands(sample_prices)

    assert isinstance(bb_df, pd.DataFrame)
    assert 'bb_upper' in bb_df.columns
    assert 'bb_middle' in bb_df.columns
    assert 'bb_lower' in bb_df.columns
    # Upper band should be above lower band
    assert (bb_df['bb_upper'].dropna() >= bb_df['bb_lower'].dropna()).all()

def test_vix_regime_features(sample_prices):
    """Test VIX regime features."""
    vix_features = vix_regime_features(sample_prices)

    assert isinstance(vix_features, pd.DataFrame)
    assert 'vix' in vix_features.columns
    assert 'low_vol_regime' in vix_features.columns
    assert 'high_vol_regime' in vix_features.columns
