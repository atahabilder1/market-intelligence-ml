"""
Backtesting Service
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from typing import List, Dict, Any

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from src.data.fetch_data import fetch_multiple_assets
from src.backtest.metrics import calculate_all_metrics
from backend.app.services.prediction_service import PredictionService

class BacktestService:
    """Service for backtesting trading strategies"""

    def __init__(self):
        self.prediction_service = PredictionService()

    def run_backtest(
        self,
        symbols: List[str],
        model_type: str,
        start_date: str,
        end_date: str,
        initial_capital: float = 100000.0,
        transaction_cost: float = 0.001,
        rebalance_frequency: str = "daily"
    ) -> Dict[str, Any]:
        """
        Run backtesting simulation.

        Parameters:
        -----------
        symbols : List[str]
            Assets to trade
        model_type : str
            ML model to use
        start_date : str
            Backtest start date
        end_date : str
            Backtest end date
        initial_capital : float
            Starting capital
        transaction_cost : float
            Transaction cost (as decimal, e.g., 0.001 = 0.1%)
        rebalance_frequency : str
            How often to rebalance (daily, weekly, monthly)

        Returns:
        --------
        Dict: Backtest results with metrics and equity curve
        """
        # Fetch data for all symbols
        data_dict = fetch_multiple_assets(symbols, start_date, end_date)

        # Train models
        for symbol in symbols:
            self.prediction_service.train_model(
                symbol=symbol,
                model_type=model_type,
                start_date=start_date,
                end_date=end_date,
                horizon="1d"
            )

        # Initialize portfolio
        portfolio_value = [initial_capital]
        portfolio_dates = []
        trades = []
        positions = {symbol: 0 for symbol in symbols}
        cash = initial_capital

        # Get all dates (use first symbol as reference)
        dates = data_dict[symbols[0]].index

        # Walk through time
        for i in range(100, len(dates)):  # Start after 100 days for feature calculation
            current_date = dates[i]
            portfolio_dates.append(current_date)

            # Get predictions for all symbols
            predictions = {}
            for symbol in symbols:
                try:
                    # Get data up to current date
                    hist_data = data_dict[symbol].iloc[:i+1]

                    # Prepare features
                    features = self.prediction_service.prepare_features(symbol, hist_data)

                    if len(features) < 20:  # Need minimum history
                        continue

                    # Get model
                    model_key = f"{symbol}_{model_type}_1d"
                    if model_key not in self.prediction_service.trained_models:
                        continue

                    model_info = self.prediction_service.trained_models[model_key]
                    model = model_info["model"]

                    # Predict
                    # Only use features that exist in both
                    available_features = [f for f in model_info["features"] if f in features.columns]
                    if len(available_features) == 0:
                        continue

                    latest_features = features.iloc[-1:][available_features]
                    pred = model.predict(latest_features)[0]
                    predictions[symbol] = pred

                except Exception as e:
                    print(f"Error predicting for {symbol}: {str(e)}")
                    continue

            # Trading logic: Equal-weight long positions in top predicted assets
            if predictions:
                # Sort by predicted return
                sorted_preds = sorted(predictions.items(), key=lambda x: x[1], reverse=True)

                # Get top 2 symbols with positive predictions
                buy_symbols = [s for s, p in sorted_preds if p > 0.01][:2]

                # Sell current positions not in buy list
                for symbol in list(positions.keys()):
                    if positions[symbol] > 0 and symbol not in buy_symbols:
                        # Sell
                        sell_price = data_dict[symbol].loc[current_date, 'Close']
                        proceeds = positions[symbol] * sell_price
                        proceeds -= proceeds * transaction_cost  # Transaction cost
                        cash += proceeds
                        trades.append({
                            "date": str(current_date),
                            "symbol": symbol,
                            "action": "SELL",
                            "quantity": positions[symbol],
                            "price": float(sell_price),
                            "value": float(proceeds)
                        })
                        positions[symbol] = 0

                # Buy new positions
                if buy_symbols:
                    allocation_per_symbol = cash * 0.95 / len(buy_symbols)  # Keep 5% cash

                    for symbol in buy_symbols:
                        buy_price = data_dict[symbol].loc[current_date, 'Close']
                        cost = allocation_per_symbol * (1 + transaction_cost)

                        if cash >= cost:
                            shares = allocation_per_symbol / buy_price
                            positions[symbol] = shares
                            cash -= cost
                            trades.append({
                                "date": str(current_date),
                                "symbol": symbol,
                                "action": "BUY",
                                "quantity": float(shares),
                                "price": float(buy_price),
                                "value": float(allocation_per_symbol)
                            })

            # Calculate portfolio value
            total_value = cash
            for symbol, shares in positions.items():
                if shares > 0:
                    current_price = data_dict[symbol].loc[current_date, 'Close']
                    total_value += shares * current_price

            portfolio_value.append(total_value)

        # Calculate returns
        portfolio_series = pd.Series(portfolio_value, index=[dates[100]] + portfolio_dates)
        returns = portfolio_series.pct_change().dropna()

        # Get benchmark returns (SPY if available, otherwise first symbol)
        benchmark_symbol = "SPY" if "SPY" in symbols else symbols[0]
        benchmark_data = data_dict[benchmark_symbol].loc[portfolio_series.index]
        benchmark_returns = benchmark_data['Close'].pct_change().dropna()

        # Align returns
        common_idx = returns.index.intersection(benchmark_returns.index)
        returns = returns.loc[common_idx]
        benchmark_returns = benchmark_returns.loc[common_idx]

        # Calculate metrics
        metrics = calculate_all_metrics(returns, benchmark_returns)

        # Build equity curve
        equity_curve = [
            {
                "date": str(date),
                "value": float(val),
                "return": float((val / initial_capital - 1) * 100)
            }
            for date, val in portfolio_series.items()
        ]

        return {
            "metrics": metrics,
            "equity_curve": equity_curve,
            "trades": trades[:100],  # Limit trades in response
            "total_trades": len(trades)
        }

# Global service instance
backtest_service = BacktestService()
