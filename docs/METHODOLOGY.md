# Methodology

## Overview

This document outlines the quantitative methodology used in the Market Intelligence ML project for multi-asset return prediction and alpha generation.

## Data Collection

### Asset Universe
- **Equities**: SPY, XLK, XLF, XLV, XLE, XLI (S&P 500 and sectors)
- **Fixed Income**: TLT (20Y+ Treasury), IEF (7-10Y Treasury)
- **Alternatives**: GLD (Gold), BTC, ETH, SOL (Cryptocurrencies)
- **Macro**: VIX (Volatility Index)

### Data Sources
- **Traditional Assets**: Yahoo Finance (yfinance)
- **Cryptocurrencies**: Binance via CCXT
- **Timeframe**: 2018-01-01 to 2025-01-01 (7 years)

## Feature Engineering

### Technical Indicators (~40 features)
- **Trend**: SMA (5, 10, 20, 50, 200 days), EMA (12, 26, 50)
- **Momentum**: RSI, MACD, ROC, Stochastic
- **Volatility**: Bollinger Bands, ATR, ADX
- **Volume**: OBV

### Cross-Asset Features (~25 features)
- **Correlations**: Rolling 30/60-day correlations between assets
- **Ratios**: Gold/SPY, BTC/SPY, TLT/IEF spreads
- **Relative Strength**: Sector rotation signals
- **Beta**: Rolling beta vs SPY
- **Flight-to-Quality**: Bond/Equity divergence

### Macro Features (~15 features)
- **VIX Regime**: Percentile rankings, spike detection
- **Yield Curve**: TLT/IEF spread and momentum
- **Risk Appetite**: Composite score from equity/bond/vol
- **Market Breadth**: Sector advance-decline metrics
- **Trend Regimes**: Golden/death crosses, MA distances

## Model Architecture

### 1. Baseline Models
**Linear Regression**
- Purpose: Establish performance floor
- Regularization: Ridge (α=1.0) and Lasso variants
- Features: All 80+ engineered features

**Random Forest**
- Trees: 100
- Max Depth: 10
- Min Samples Split: 5
- Purpose: Feature importance analysis

### 2. Gradient Boosting (XGBoost)
**Primary Model**
- Estimators: 100
- Max Depth: 5
- Learning Rate: 0.01
- Subsample: 0.8
- Col Sample: 0.8
- Early Stopping: 10 rounds on validation set

### 3. Deep Learning (LSTM)
**Architecture**
- Input: Sequences of 20 time steps
- LSTM Layers: [64, 32] units with dropout (0.2)
- Output: Dense(1) for return prediction
- Optimizer: Adam (lr=0.001)
- Early Stopping: Patience 10

### 4. Ensemble Model
**Stacking Approach**
- Base Models: LinearReg, RandomForest, XGBoost, LSTM
- Meta-Learner: Ridge Regression
- Training: Out-of-fold predictions on validation set
- Weighting: Learned via meta-model

## Training Strategy

### Data Splits
- **Training**: 2018-01-01 to 2023-12-31 (6 years)
- **Validation**: 2024-01-01 to 2024-06-30 (6 months)
- **Test**: 2024-07-01 to 2025-01-01 (6 months)

### Walk-Forward Validation
- Initial Training Window: 252 days (1 year)
- Step Size: 21 days (1 month)
- Retraining Frequency: 63 days (3 months)
- Prevents look-ahead bias

### Cross-Validation
- Method: TimeSeriesSplit
- Folds: 5
- Preserves temporal ordering

## Backtesting Framework

### Position Sizing
- Predictions normalized to [-1, 1] via z-score
- Long/Short based on sign
- Size proportional to prediction confidence

### Transaction Costs
- Commission: 10 basis points (0.001)
- Slippage: 5 basis points (0.0005)
- Total: 15 bps per trade

### Performance Metrics
**Risk-Adjusted**
- Sharpe Ratio (target: >1.0)
- Sortino Ratio
- Calmar Ratio
- Information Ratio (vs SPY, target: >0.5)

**Returns**
- Total Return
- Annualized Return (target: >5%)
- Max Drawdown (target: <25%)

**Prediction Quality**
- Directional Accuracy (target: >55%)
- MSE, MAE, R²

## Risk Management

### Constraints
- Maximum position size: 100% (full notional)
- No leverage
- Daily rebalancing

### Monitoring
- Rolling Sharpe (30-day window)
- Drawdown tracking
- Correlation stability

## Implementation Notes

### Feature Selection
- Correlation threshold: |ρ| < 0.95 (remove highly correlated)
- Variance threshold: σ² > 0.01
- Importance filtering: Keep top 50 features from Random Forest

### Hyperparameter Tuning
- Method: Grid Search with TimeSeriesSplit
- Metric: Negative MSE
- Parallelization: All CPU cores

### Production Considerations
- Model persistence: Pickle/Joblib
- Retraining: Quarterly
- Monitoring: Weekly performance review
- Alerts: Sharpe < 0.5 or Drawdown > 20%

## References

1. Gu, S., Kelly, B., & Xiu, D. (2020). "Empirical Asset Pricing via Machine Learning." *Review of Financial Studies*.
2. López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley.
3. Jansen, S. (2020). *Machine Learning for Algorithmic Trading*. Packt.
