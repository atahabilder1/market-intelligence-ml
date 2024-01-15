"""
Performance metrics for backtesting.
"""

import pandas as pd
import numpy as np
from typing import Union

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sharpe Ratio.

    Parameters:
    -----------
    returns : pd.Series or np.ndarray
        Daily returns
    risk_free_rate : float
        Annual risk-free rate

    Returns:
    --------
    float: Sharpe ratio
    """
    if isinstance(returns, pd.Series):
        returns = returns.values

    excess_returns = returns - (risk_free_rate / 252)
    if returns.std() == 0:
        return 0.0

    sharpe = np.sqrt(252) * excess_returns.mean() / returns.std()
    return sharpe

def calculate_sortino_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sortino Ratio (uses downside deviation).

    Parameters:
    -----------
    returns : pd.Series or np.ndarray
        Daily returns
    risk_free_rate : float
        Annual risk-free rate

    Returns:
    --------
    float: Sortino ratio
    """
    if isinstance(returns, pd.Series):
        returns = returns.values

    excess_returns = returns - (risk_free_rate / 252)
    downside_returns = returns[returns < 0]

    if len(downside_returns) == 0 or downside_returns.std() == 0:
        return 0.0

    sortino = np.sqrt(252) * excess_returns.mean() / downside_returns.std()
    return sortino

def calculate_max_drawdown(returns):
    """
    Calculate maximum drawdown.

    Parameters:
    -----------
    returns : pd.Series or np.ndarray
        Daily returns

    Returns:
    --------
    float: Maximum drawdown (negative value)
    """
    if isinstance(returns, np.ndarray):
        returns = pd.Series(returns)

    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max

    return drawdown.min()

def calculate_calmar_ratio(returns):
    """
    Calculate Calmar Ratio (annualized return / max drawdown).

    Parameters:
    -----------
    returns : pd.Series or np.ndarray
        Daily returns

    Returns:
    --------
    float: Calmar ratio
    """
    annual_return = (1 + returns).prod() ** (252 / len(returns)) - 1
    max_dd = abs(calculate_max_drawdown(returns))

    if max_dd == 0:
        return 0.0

    return annual_return / max_dd

def calculate_information_ratio(returns, benchmark_returns):
    """
    Calculate Information Ratio.

    Parameters:
    -----------
    returns : pd.Series
        Strategy returns
    benchmark_returns : pd.Series
        Benchmark returns

    Returns:
    --------
    float: Information ratio
    """
    active_returns = returns - benchmark_returns
    tracking_error = active_returns.std() * np.sqrt(252)

    if tracking_error == 0:
        return 0.0

    return (active_returns.mean() * 252) / tracking_error

def calculate_win_rate(returns):
    """
    Calculate win rate (percentage of positive returns).

    Parameters:
    -----------
    returns : pd.Series or np.ndarray
        Daily returns

    Returns:
    --------
    float: Win rate (0 to 1)
    """
    if isinstance(returns, pd.Series):
        returns = returns.values

    returns = returns[returns != 0]  # Exclude zero returns
    if len(returns) == 0:
        return 0.0

    return (returns > 0).sum() / len(returns)

def calculate_profit_factor(returns):
    """
    Calculate profit factor (gross profit / gross loss).

    Parameters:
    -----------
    returns : pd.Series or np.ndarray
        Daily returns

    Returns:
    --------
    float: Profit factor
    """
    if isinstance(returns, pd.Series):
        returns = returns.values

    gross_profit = returns[returns > 0].sum()
    gross_loss = abs(returns[returns < 0].sum())

    if gross_loss == 0:
        return np.inf if gross_profit > 0 else 0.0

    return gross_profit / gross_loss

def calculate_alpha_beta(returns, benchmark_returns, risk_free_rate=0.02):
    """
    Calculate Jensen's Alpha and Beta.

    Parameters:
    -----------
    returns : pd.Series
        Strategy returns
    benchmark_returns : pd.Series
        Benchmark returns
    risk_free_rate : float
        Annual risk-free rate

    Returns:
    --------
    dict: {'alpha': float, 'beta': float}
    """
    # Annualize risk-free rate to daily
    rf_daily = risk_free_rate / 252

    # Excess returns
    excess_strategy = returns - rf_daily
    excess_benchmark = benchmark_returns - rf_daily

    # Calculate beta
    covariance = excess_strategy.cov(excess_benchmark)
    benchmark_variance = excess_benchmark.var()

    if benchmark_variance == 0:
        beta = 0.0
    else:
        beta = covariance / benchmark_variance

    # Calculate alpha (annualized)
    alpha = (excess_strategy.mean() - beta * excess_benchmark.mean()) * 252

    return {'alpha': alpha, 'beta': beta}

def calculate_all_metrics(returns, benchmark_returns=None):
    """
    Calculate all performance metrics.

    Parameters:
    -----------
    returns : pd.Series
        Strategy returns
    benchmark_returns : pd.Series, optional
        Benchmark returns

    Returns:
    --------
    dict: Dictionary of all metrics
    """
    metrics = {}

    # Return metrics
    total_return = (1 + returns).prod() - 1
    annual_return = (1 + returns).prod() ** (252 / len(returns)) - 1

    metrics['total_return'] = total_return
    metrics['annual_return'] = annual_return
    metrics['volatility'] = returns.std() * np.sqrt(252)

    # Risk-adjusted metrics
    metrics['sharpe_ratio'] = calculate_sharpe_ratio(returns)
    metrics['sortino_ratio'] = calculate_sortino_ratio(returns)
    metrics['calmar_ratio'] = calculate_calmar_ratio(returns)

    # Drawdown metrics
    metrics['max_drawdown'] = calculate_max_drawdown(returns)

    # Win/loss metrics
    metrics['win_rate'] = calculate_win_rate(returns)
    metrics['profit_factor'] = calculate_profit_factor(returns)

    # Benchmark-relative metrics
    if benchmark_returns is not None:
        metrics['information_ratio'] = calculate_information_ratio(returns, benchmark_returns)
        alpha_beta = calculate_alpha_beta(returns, benchmark_returns)
        metrics['alpha'] = alpha_beta['alpha']
        metrics['beta'] = alpha_beta['beta']

    return metrics

def print_performance_report(metrics, title="Performance Report"):
    """
    Print formatted performance report.

    Parameters:
    -----------
    metrics : dict
        Dictionary of performance metrics
    title : str
        Report title
    """
    print(f"\n{'=' * 60}")
    print(f"{title:^60}")
    print('=' * 60)

    print(f"\nReturn Metrics:")
    print(f"  Total Return:        {metrics.get('total_return', 0):.2%}")
    print(f"  Annual Return:       {metrics.get('annual_return', 0):.2%}")
    print(f"  Volatility (Annual): {metrics.get('volatility', 0):.2%}")

    print(f"\nRisk-Adjusted Metrics:")
    print(f"  Sharpe Ratio:   {metrics.get('sharpe_ratio', 0):.3f}")
    print(f"  Sortino Ratio:  {metrics.get('sortino_ratio', 0):.3f}")
    print(f"  Calmar Ratio:   {metrics.get('calmar_ratio', 0):.3f}")

    print(f"\nDrawdown:")
    print(f"  Max Drawdown:   {metrics.get('max_drawdown', 0):.2%}")

    print(f"\nWin/Loss:")
    print(f"  Win Rate:       {metrics.get('win_rate', 0):.2%}")
    print(f"  Profit Factor:  {metrics.get('profit_factor', 0):.2f}")

    if 'alpha' in metrics:
        print(f"\nBenchmark-Relative:")
        print(f"  Alpha:              {metrics.get('alpha', 0):.2%}")
        print(f"  Beta:               {metrics.get('beta', 0):.2f}")
        print(f"  Information Ratio:  {metrics.get('information_ratio', 0):.3f}")

    print('=' * 60)
