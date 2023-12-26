"""
Cross-asset feature engineering.
"""

import pandas as pd
import numpy as np
from typing import Dict, List

def calculate_correlation(asset1, asset2, window=30):
    """
    Calculate rolling correlation between two assets.

    Parameters:
    -----------
    asset1 : pd.Series
        First asset price series
    asset2 : pd.Series
        Second asset price series
    window : int
        Rolling window size

    Returns:
    --------
    pd.Series: Rolling correlation values
    """
    return asset1.rolling(window=window).corr(asset2)

def calculate_asset_ratios(prices_dict: Dict[str, pd.Series], base_asset='SPY'):
    """
    Calculate cross-asset ratios relative to a base asset.

    Parameters:
    -----------
    prices_dict : dict
        Dictionary of asset names to price series
    base_asset : str
        Base asset for ratio calculation

    Returns:
    --------
    pd.DataFrame: Ratios for all assets
    """
    ratios = pd.DataFrame()

    if base_asset not in prices_dict:
        raise ValueError(f"Base asset {base_asset} not found in prices")

    base_price = prices_dict[base_asset]

    for asset, price in prices_dict.items():
        if asset != base_asset:
            ratios[f'{asset}_{base_asset}_ratio'] = price / base_price
            # Also calculate momentum of the ratio
            ratios[f'{asset}_{base_asset}_ratio_mom'] = ratios[f'{asset}_{base_asset}_ratio'].pct_change(20)

    return ratios

def sector_rotation_signals(sector_data: Dict[str, pd.Series], window=20):
    """
    Generate sector rotation signals based on relative strength.

    Parameters:
    -----------
    sector_data : dict
        Dictionary of sector names to price series
    window : int
        Window for momentum calculation

    Returns:
    --------
    pd.DataFrame: Sector rotation signals
    """
    signals = pd.DataFrame()

    # Calculate momentum for each sector
    momentum = {}
    for sector, prices in sector_data.items():
        momentum[sector] = prices.pct_change(window)

    momentum_df = pd.DataFrame(momentum)

    # Rank sectors by momentum
    signals['strongest_sector'] = momentum_df.idxmax(axis=1)
    signals['weakest_sector'] = momentum_df.idxmin(axis=1)
    signals['momentum_spread'] = momentum_df.max(axis=1) - momentum_df.min(axis=1)

    # Calculate sector relative strength
    for sector in sector_data.keys():
        sector_mean = momentum_df[sector]
        market_mean = momentum_df.mean(axis=1)
        signals[f'{sector}_relative_strength'] = sector_mean - market_mean

    return signals

def calculate_correlation_matrix(prices_dict: Dict[str, pd.Series], window=60):
    """
    Calculate rolling correlation matrix for multiple assets.

    Parameters:
    -----------
    prices_dict : dict
        Dictionary of asset names to price series
    window : int
        Rolling window size

    Returns:
    --------
    dict: Dictionary of correlation dataframes for each asset pair
    """
    correlations = {}
    assets = list(prices_dict.keys())

    for i, asset1 in enumerate(assets):
        for asset2 in assets[i+1:]:
            corr_key = f'{asset1}_{asset2}_corr'
            correlations[corr_key] = calculate_correlation(
                prices_dict[asset1],
                prices_dict[asset2],
                window
            )

    return pd.DataFrame(correlations)

def calculate_beta(asset, market, window=60):
    """
    Calculate rolling beta of an asset relative to market.

    Parameters:
    -----------
    asset : pd.Series
        Asset price series
    market : pd.Series
        Market index price series
    window : int
        Rolling window size

    Returns:
    --------
    pd.Series: Rolling beta values
    """
    asset_returns = asset.pct_change()
    market_returns = market.pct_change()

    # Calculate covariance and variance
    covariance = asset_returns.rolling(window=window).cov(market_returns)
    market_variance = market_returns.rolling(window=window).var()

    beta = covariance / market_variance
    return beta

def calculate_spread(asset1, asset2):
    """
    Calculate price spread between two assets.

    Parameters:
    -----------
    asset1 : pd.Series
        First asset price series
    asset2 : pd.Series
        Second asset price series

    Returns:
    --------
    pd.DataFrame: Spread, z-score, and mean reversion signals
    """
    spread = asset1 - asset2

    spread_df = pd.DataFrame()
    spread_df['spread'] = spread
    spread_df['spread_ma'] = spread.rolling(window=20).mean()
    spread_df['spread_std'] = spread.rolling(window=20).std()
    spread_df['spread_zscore'] = (spread - spread_df['spread_ma']) / spread_df['spread_std']

    return spread_df

def calculate_regime_features(prices_dict: Dict[str, pd.Series], vix_series=None):
    """
    Calculate market regime features.

    Parameters:
    -----------
    prices_dict : dict
        Dictionary of asset prices
    vix_series : pd.Series, optional
        VIX volatility index

    Returns:
    --------
    pd.DataFrame: Market regime indicators
    """
    regime = pd.DataFrame()

    # Volatility regime
    if vix_series is not None:
        regime['vix_level'] = vix_series
        regime['high_vol_regime'] = (vix_series > vix_series.rolling(60).quantile(0.75)).astype(int)
        regime['low_vol_regime'] = (vix_series < vix_series.rolling(60).quantile(0.25)).astype(int)

    # Trend regime (using SPY if available)
    if 'SPY' in prices_dict:
        spy = prices_dict['SPY']
        regime['spy_above_ma200'] = (spy > spy.rolling(200).mean()).astype(int)
        regime['spy_above_ma50'] = (spy > spy.rolling(50).mean()).astype(int)
        regime['bull_market'] = ((spy > spy.rolling(200).mean()) &
                                 (spy.rolling(50).mean() > spy.rolling(200).mean())).astype(int)

    # Cross-asset dispersion
    if len(prices_dict) > 1:
        returns = pd.DataFrame({k: v.pct_change() for k, v in prices_dict.items()})
        regime['cross_asset_dispersion'] = returns.std(axis=1)

    return regime

def calculate_relative_performance(prices_dict: Dict[str, pd.Series], periods=[5, 20, 60]):
    """
    Calculate relative performance across multiple time periods.

    Parameters:
    -----------
    prices_dict : dict
        Dictionary of asset prices
    periods : list
        List of periods for performance calculation

    Returns:
    --------
    pd.DataFrame: Relative performance metrics
    """
    perf = pd.DataFrame()

    for period in periods:
        returns = {}
        for asset, prices in prices_dict.items():
            returns[asset] = prices.pct_change(period)

        returns_df = pd.DataFrame(returns)

        # Rank performance
        perf[f'rank_{period}d'] = returns_df.rank(axis=1, pct=True).mean(axis=1)
        perf[f'top_performer_{period}d'] = returns_df.idxmax(axis=1)
        perf[f'bottom_performer_{period}d'] = returns_df.idxmin(axis=1)
        perf[f'performance_spread_{period}d'] = returns_df.max(axis=1) - returns_df.min(axis=1)

    return perf

def calculate_flight_to_quality(equity_price, bond_price, gold_price=None):
    """
    Calculate flight-to-quality indicators.

    Parameters:
    -----------
    equity_price : pd.Series
        Equity index price (e.g., SPY)
    bond_price : pd.Series
        Bond price (e.g., TLT)
    gold_price : pd.Series, optional
        Gold price

    Returns:
    --------
    pd.DataFrame: Flight-to-quality signals
    """
    ftq = pd.DataFrame()

    # Equity-Bond correlation (negative during flight to quality)
    ftq['equity_bond_corr'] = calculate_correlation(equity_price, bond_price, window=20)

    # Bond outperformance
    equity_returns = equity_price.pct_change(5)
    bond_returns = bond_price.pct_change(5)
    ftq['bond_outperformance'] = bond_returns - equity_returns

    if gold_price is not None:
        gold_returns = gold_price.pct_change(5)
        ftq['gold_outperformance'] = gold_returns - equity_returns
        ftq['safe_haven_composite'] = (ftq['bond_outperformance'] + ftq['gold_outperformance']) / 2

    return ftq
