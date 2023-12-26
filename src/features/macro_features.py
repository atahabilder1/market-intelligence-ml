"""
Macro economic feature engineering.
"""

import pandas as pd
import numpy as np

def calculate_yield_spread(long_term, short_term):
    """
    Calculate yield spread between long-term and short-term bonds.

    Parameters:
    -----------
    long_term : pd.Series
        Long-term bond prices (e.g., TLT for 20Y+)
    short_term : pd.Series
        Short-term bond prices (e.g., IEF for 7-10Y)

    Returns:
    --------
    pd.DataFrame: Yield spread features
    """
    spread_df = pd.DataFrame()

    # Price ratio as proxy for yield spread (inverse relationship)
    spread_df['bond_spread'] = long_term / short_term

    # Changes in spread
    spread_df['spread_change'] = spread_df['bond_spread'].diff()
    spread_df['spread_momentum'] = spread_df['bond_spread'].pct_change(20)

    # Spread relative to history
    spread_df['spread_zscore'] = (
        (spread_df['bond_spread'] - spread_df['bond_spread'].rolling(60).mean()) /
        spread_df['bond_spread'].rolling(60).std()
    )

    # Yield curve steepening/flattening
    spread_df['curve_steepening'] = (spread_df['spread_change'] > 0).astype(int)

    return spread_df

def vix_regime_features(vix_data):
    """
    Generate VIX-based regime and fear features.

    Parameters:
    -----------
    vix_data : pd.Series
        VIX index values

    Returns:
    --------
    pd.DataFrame: VIX regime features
    """
    vix_features = pd.DataFrame(index=vix_data.index)

    # Raw VIX levels
    vix_features['vix'] = vix_data
    vix_features['vix_ma_20'] = vix_data.rolling(20).mean()
    vix_features['vix_ma_50'] = vix_data.rolling(50).mean()

    # VIX percentile ranking
    vix_features['vix_percentile_60d'] = vix_data.rolling(60).apply(
        lambda x: (x[-1] <= x).sum() / len(x) * 100
    )
    vix_features['vix_percentile_252d'] = vix_data.rolling(252).apply(
        lambda x: (x[-1] <= x).sum() / len(x) * 100
    )

    # VIX regimes
    vix_features['low_vol_regime'] = (vix_data < 15).astype(int)
    vix_features['normal_vol_regime'] = ((vix_data >= 15) & (vix_data < 25)).astype(int)
    vix_features['high_vol_regime'] = ((vix_data >= 25) & (vix_data < 35)).astype(int)
    vix_features['extreme_vol_regime'] = (vix_data >= 35).astype(int)

    # VIX momentum and rate of change
    vix_features['vix_roc_5d'] = vix_data.pct_change(5)
    vix_features['vix_roc_20d'] = vix_data.pct_change(20)

    # VIX spike detection
    vix_features['vix_spike'] = (vix_data > vix_data.rolling(20).mean() + 2 * vix_data.rolling(20).std()).astype(int)

    # Term structure (VIX vs VIX MA - contango/backwardation proxy)
    vix_features['vix_term_structure'] = vix_data - vix_features['vix_ma_20']

    # Mean reversion signals
    vix_features['vix_zscore'] = (vix_data - vix_features['vix_ma_50']) / vix_data.rolling(50).std()
    vix_features['vix_mean_reversion_signal'] = (vix_features['vix_zscore'] > 2).astype(int)

    return vix_features

def calculate_risk_appetite(equity_index, vix_data, bond_index):
    """
    Calculate risk appetite indicators.

    Parameters:
    -----------
    equity_index : pd.Series
        Equity index prices (e.g., SPY)
    vix_data : pd.Series
        VIX volatility index
    bond_index : pd.Series
        Bond index prices (e.g., TLT)

    Returns:
    --------
    pd.DataFrame: Risk appetite indicators
    """
    risk_df = pd.DataFrame()

    # Returns
    equity_returns = equity_index.pct_change(20)
    bond_returns = bond_index.pct_change(20)

    # Risk-on/risk-off indicator
    risk_df['equity_bond_ratio'] = equity_index / bond_index
    risk_df['risk_on_signal'] = (
        (equity_returns > bond_returns) &
        (vix_data < vix_data.rolling(60).quantile(0.5))
    ).astype(int)

    # Inverse VIX as risk appetite proxy
    risk_df['inverse_vix'] = 100 / vix_data

    # Risk appetite composite
    vix_normalized = (vix_data - vix_data.rolling(252).min()) / (vix_data.rolling(252).max() - vix_data.rolling(252).min())
    equity_mom_normalized = (equity_returns - equity_returns.rolling(252).min()) / (equity_returns.rolling(252).max() - equity_returns.rolling(252).min())

    risk_df['risk_appetite_score'] = (1 - vix_normalized) * 0.5 + equity_mom_normalized * 0.5

    return risk_df

def calculate_volatility_features(prices, window=20):
    """
    Calculate various volatility measures.

    Parameters:
    -----------
    prices : pd.Series
        Price series
    window : int
        Rolling window for calculations

    Returns:
    --------
    pd.DataFrame: Volatility features
    """
    vol_df = pd.DataFrame()

    returns = prices.pct_change()

    # Historical volatility (annualized)
    vol_df['realized_vol'] = returns.rolling(window).std() * np.sqrt(252)

    # Parkinson volatility (using high-low range if available)
    vol_df['vol_expanding'] = returns.expanding().std() * np.sqrt(252)

    # Volatility of volatility
    vol_df['vol_of_vol'] = vol_df['realized_vol'].rolling(window).std()

    # Volatility ratio (short vs long term)
    vol_short = returns.rolling(10).std()
    vol_long = returns.rolling(50).std()
    vol_df['vol_ratio'] = vol_short / vol_long

    # Volatility regime
    vol_df['high_vol'] = (vol_df['realized_vol'] > vol_df['realized_vol'].rolling(60).quantile(0.75)).astype(int)
    vol_df['low_vol'] = (vol_df['realized_vol'] < vol_df['realized_vol'].rolling(60).quantile(0.25)).astype(int)

    return vol_df

def calculate_market_breadth(sector_prices_dict):
    """
    Calculate market breadth indicators from sector data.

    Parameters:
    -----------
    sector_prices_dict : dict
        Dictionary of sector names to price series

    Returns:
    --------
    pd.DataFrame: Market breadth indicators
    """
    breadth_df = pd.DataFrame()

    # Calculate sector returns
    sector_returns = {}
    for sector, prices in sector_prices_dict.items():
        sector_returns[sector] = prices.pct_change(20)

    returns_df = pd.DataFrame(sector_returns)

    # Percentage of sectors in uptrend
    breadth_df['pct_sectors_positive'] = (returns_df > 0).sum(axis=1) / len(sector_prices_dict)

    # Sector advance-decline line
    breadth_df['sector_advance_decline'] = (returns_df > 0).sum(axis=1) - (returns_df < 0).sum(axis=1)
    breadth_df['sector_ad_line'] = breadth_df['sector_advance_decline'].cumsum()

    # Dispersion across sectors
    breadth_df['sector_dispersion'] = returns_df.std(axis=1)

    # Breadth thrust (rapid improvement in breadth)
    breadth_df['breadth_thrust'] = (
        breadth_df['pct_sectors_positive'].diff(10) > 0.3
    ).astype(int)

    # Strong breadth regime
    breadth_df['strong_breadth'] = (breadth_df['pct_sectors_positive'] > 0.7).astype(int)
    breadth_df['weak_breadth'] = (breadth_df['pct_sectors_positive'] < 0.3).astype(int)

    return breadth_df

def calculate_momentum_regime(prices, fast=50, slow=200):
    """
    Calculate trend/momentum regime features.

    Parameters:
    -----------
    prices : pd.Series
        Price series
    fast : int
        Fast moving average period
    slow : int
        Slow moving average period

    Returns:
    --------
    pd.DataFrame: Momentum regime features
    """
    regime_df = pd.DataFrame()

    ma_fast = prices.rolling(fast).mean()
    ma_slow = prices.rolling(slow).mean()

    # Trend identification
    regime_df['uptrend'] = (prices > ma_slow).astype(int)
    regime_df['strong_uptrend'] = ((prices > ma_slow) & (ma_fast > ma_slow)).astype(int)
    regime_df['downtrend'] = (prices < ma_slow).astype(int)

    # Distance from moving averages
    regime_df['pct_from_ma50'] = (prices - ma_fast) / ma_fast * 100
    regime_df['pct_from_ma200'] = (prices - ma_slow) / ma_slow * 100

    # MA crossover signals
    regime_df['golden_cross'] = ((ma_fast > ma_slow) & (ma_fast.shift(1) <= ma_slow.shift(1))).astype(int)
    regime_df['death_cross'] = ((ma_fast < ma_slow) & (ma_fast.shift(1) >= ma_slow.shift(1))).astype(int)

    # Trend strength
    returns = prices.pct_change(20)
    regime_df['trend_strength'] = np.abs(returns)

    return regime_df
