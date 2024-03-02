"""
Backtesting engine for strategy evaluation.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
from src.backtest.metrics import calculate_all_metrics

class BacktestEngine:
    """Walk-forward backtesting with transaction costs."""

    def __init__(self, transaction_cost=0.001, slippage=0.0005, initial_capital=100000):
        """
        Initialize backtest engine.

        Parameters:
        -----------
        transaction_cost : float
            Transaction cost as a fraction (e.g., 0.001 = 10 bps)
        slippage : float
            Slippage as a fraction
        initial_capital : float
            Starting capital
        """
        self.transaction_cost = transaction_cost
        self.slippage = slippage
        self.initial_capital = initial_capital

    def run_backtest(self, predictions, actual_returns, positions=None):
        """
        Run backtest given predictions and actual returns.

        Parameters:
        -----------
        predictions : pd.Series or np.ndarray
            Model predictions (expected returns)
        actual_returns : pd.Series
            Actual returns
        positions : pd.Series, optional
            Explicit position sizes (if None, derived from predictions)

        Returns:
        --------
        dict: Backtest results including returns, positions, and metrics
        """
        if isinstance(predictions, np.ndarray):
            predictions = pd.Series(predictions, index=actual_returns.index)

        # Generate positions from predictions if not provided
        if positions is None:
            positions = self._predictions_to_positions(predictions)

        # Calculate strategy returns
        strategy_returns = self._calculate_strategy_returns(positions, actual_returns)

        # Calculate metrics
        metrics = calculate_all_metrics(strategy_returns, actual_returns)

        # Calculate equity curve
        equity_curve = (1 + strategy_returns).cumprod() * self.initial_capital

        return {
            'returns': strategy_returns,
            'positions': positions,
            'equity_curve': equity_curve,
            'metrics': metrics,
            'predictions': predictions
        }

    def _predictions_to_positions(self, predictions):
        """
        Convert predictions to position sizes.

        Parameters:
        -----------
        predictions : pd.Series
            Model predictions

        Returns:
        --------
        pd.Series: Position sizes (-1 to 1)
        """
        # Simple approach: long if positive prediction, short if negative
        positions = pd.Series(index=predictions.index, dtype=float)

        # Normalize predictions to [-1, 1] range
        pred_clean = predictions.dropna()
        if len(pred_clean) > 0:
            # Z-score normalization
            pred_mean = pred_clean.mean()
            pred_std = pred_clean.std()

            if pred_std > 0:
                positions = (predictions - pred_mean) / pred_std
                # Clip to [-1, 1]
                positions = positions.clip(-1, 1)
            else:
                positions = np.sign(predictions)
        else:
            positions[:] = 0

        return positions

    def _calculate_strategy_returns(self, positions, actual_returns):
        """
        Calculate strategy returns including transaction costs.

        Parameters:
        -----------
        positions : pd.Series
            Position sizes
        actual_returns : pd.Series
            Actual market returns

        Returns:
        --------
        pd.Series: Strategy returns
        """
        # Position changes (for transaction costs)
        position_changes = positions.diff().abs()

        # Gross returns (before costs)
        gross_returns = positions.shift(1) * actual_returns

        # Transaction costs
        costs = position_changes * (self.transaction_cost + self.slippage)

        # Net returns
        net_returns = gross_returns - costs

        return net_returns.fillna(0)

    def walk_forward_backtest(self, model, X, y, train_size=252, step_size=21,
                              retrain_frequency=63):
        """
        Perform walk-forward backtesting.

        Parameters:
        -----------
        model : object
            Model with fit() and predict() methods
        X : pd.DataFrame
            Features
        y : pd.Series
            Target returns
        train_size : int
            Initial training window size (days)
        step_size : int
            Step size for rolling window (days)
        retrain_frequency : int
            How often to retrain model (days)

        Returns:
        --------
        dict: Walk-forward backtest results
        """
        n_samples = len(X)
        predictions = pd.Series(index=X.index, dtype=float)
        actual_returns_list = []

        last_train_idx = 0

        for i in range(train_size, n_samples, step_size):
            # Retrain if necessary
            if i - last_train_idx >= retrain_frequency:
                X_train = X.iloc[:i]
                y_train = y.iloc[:i]
                model.fit(X_train, y_train)
                last_train_idx = i

            # Predict
            end_idx = min(i + step_size, n_samples)
            X_test = X.iloc[i:end_idx]

            preds = model.predict(X_test)

            # Store predictions
            predictions.iloc[i:end_idx] = preds if isinstance(preds, np.ndarray) else preds

            # Store actual returns
            actual_returns_list.extend(y.iloc[i:end_idx].values)

        # Get actual returns for prediction period
        actual_returns = y.loc[predictions.dropna().index]

        # Run backtest
        results = self.run_backtest(predictions.dropna(), actual_returns)
        results['walk_forward_info'] = {
            'train_size': train_size,
            'step_size': step_size,
            'retrain_frequency': retrain_frequency
        }

        return results

    def plot_results(self, results, benchmark_returns=None):
        """
        Plot backtest results.

        Parameters:
        -----------
        results : dict
            Backtest results
        benchmark_returns : pd.Series, optional
            Benchmark returns for comparison
        """
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(3, 1, figsize=(14, 10))

        # Equity curve
        axes[0].plot(results['equity_curve'], label='Strategy', linewidth=2)
        if benchmark_returns is not None:
            benchmark_equity = (1 + benchmark_returns).cumprod() * self.initial_capital
            axes[0].plot(benchmark_equity, label='Benchmark', linewidth=2, alpha=0.7)
        axes[0].set_ylabel('Portfolio Value ($)')
        axes[0].set_title('Equity Curve')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Returns distribution
        axes[1].hist(results['returns'].dropna(), bins=50, alpha=0.7, edgecolor='black')
        axes[1].axvline(results['returns'].mean(), color='red', linestyle='--',
                        label=f"Mean: {results['returns'].mean():.4f}")
        axes[1].set_xlabel('Returns')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title('Returns Distribution')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        # Drawdown
        cumulative = results['equity_curve'] / self.initial_capital
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max

        axes[2].fill_between(drawdown.index, drawdown, 0, alpha=0.3, color='red')
        axes[2].plot(drawdown, color='red', linewidth=1)
        axes[2].set_ylabel('Drawdown')
        axes[2].set_xlabel('Date')
        axes[2].set_title('Drawdown')
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()
