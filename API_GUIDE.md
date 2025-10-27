# Market Intelligence ML - API Guide

Complete API reference for the FastAPI backend.

---

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

---

## Authentication

Currently, the API is open and does not require authentication. For production deployment, implement authentication using JWT tokens or API keys.

---

## Common Response Formats

### Success Response
```json
{
  "data": {},
  "message": "Success"
}
```

### Error Response
```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "detail": "Additional context"
}
```

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### 2. List Assets

**GET** `/api/assets/`

Get all available assets for trading/analysis.

**Response:**
```json
{
  "assets": [
    {
      "symbol": "SPY",
      "name": "SPDR S&P 500 ETF",
      "asset_class": "equity",
      "description": "S&P 500 Index Fund"
    }
  ],
  "total": 15
}
```

---

### 3. Get Asset Categories

**GET** `/api/assets/categories`

Get assets grouped by category.

**Response:**
```json
{
  "equities": ["SPY", "XLK", "XLF", "XLV", "XLE", "XLI"],
  "fixed_income": ["TLT", "IEF"],
  "alternatives": ["GLD"],
  "crypto": ["BTC/USDT", "ETH/USDT", "SOL/USDT"],
  "macro": ["^VIX"]
}
```

---

### 4. Generate Predictions

**POST** `/api/predict/`

Generate ML predictions for asset returns.

**Request Body:**
```json
{
  "symbols": ["SPY", "BTC/USDT"],
  "model_type": "xgboost",
  "horizon": "1d",
  "start_date": "2023-01-01",
  "end_date": "2024-12-31"
}
```

**Parameters:**
- `symbols` (required): List of asset symbols
- `model_type` (optional): Model to use
  - `xgboost` (default, recommended)
  - `random_forest`
  - `linear`
  - `lstm`
  - `ensemble`
- `horizon` (optional): Prediction timeframe
  - `1d` (default): 1 day
  - `5d`: 5 days
  - `20d`: 20 days
  - `60d`: 60 days
- `start_date` (optional): Training data start
- `end_date` (optional): Training data end

**Response:**
```json
{
  "predictions": [
    {
      "symbol": "SPY",
      "predicted_return": 0.023,
      "confidence": 0.78,
      "signal": "BUY",
      "current_price": 450.25,
      "predicted_price": 460.60,
      "features_used": 85,
      "model_used": "xgboost"
    }
  ],
  "timestamp": "2024-01-15T10:30:00",
  "model_info": {
    "model_type": "xgboost",
    "horizon": "1d",
    "total_symbols": 2
  }
}
```

**Signal Types:**
- `BUY`: Predicted return > 2%
- `SELL`: Predicted return < -2%
- `HOLD`: Predicted return between -2% and 2%

---

### 5. Get Feature Importance

**GET** `/api/predict/feature-importance/{symbol}`

Get feature importance for a trained model.

**Parameters:**
- `symbol` (path): Asset symbol
- `model_type` (query, optional): Model type (default: xgboost)
- `horizon` (query, optional): Horizon (default: 1d)
- `top_n` (query, optional): Number of features (default: 20)

**Response:**
```json
{
  "symbol": "SPY",
  "model_type": "xgboost",
  "features": [
    {
      "feature_name": "rsi",
      "importance": 0.15,
      "rank": 1
    },
    {
      "feature_name": "macd",
      "importance": 0.12,
      "rank": 2
    }
  ]
}
```

---

### 6. Run Backtest

**POST** `/api/backtest/`

Run a backtesting simulation of a trading strategy.

**Request Body:**
```json
{
  "symbols": ["SPY"],
  "model_type": "xgboost",
  "start_date": "2020-01-01",
  "end_date": "2024-12-31",
  "initial_capital": 100000,
  "transaction_cost": 0.001,
  "rebalance_frequency": "daily"
}
```

**Parameters:**
- `symbols` (required): Assets to trade
- `model_type` (optional): ML model (default: xgboost)
- `start_date` (required): Backtest start
- `end_date` (required): Backtest end
- `initial_capital` (optional): Starting capital (default: 100000)
- `transaction_cost` (optional): Cost as decimal (default: 0.001 = 0.1%)
- `rebalance_frequency` (optional): Rebalancing frequency (default: daily)

**Response:**
```json
{
  "metrics": {
    "total_return": 0.45,
    "annual_return": 0.12,
    "volatility": 0.18,
    "sharpe_ratio": 1.35,
    "sortino_ratio": 1.82,
    "calmar_ratio": 0.95,
    "max_drawdown": -0.15,
    "win_rate": 0.58,
    "profit_factor": 1.65,
    "alpha": 0.08,
    "beta": 0.92,
    "information_ratio": 0.55
  },
  "equity_curve": [
    {
      "date": "2020-01-02",
      "value": 100000,
      "return": 0.0
    },
    {
      "date": "2020-01-03",
      "value": 101250,
      "return": 1.25
    }
  ],
  "trades": [
    {
      "date": "2020-01-02",
      "symbol": "SPY",
      "action": "BUY",
      "quantity": 220.5,
      "price": 320.50,
      "value": 70670.25
    }
  ],
  "model_type": "xgboost",
  "symbols": ["SPY"],
  "start_date": "2020-01-01",
  "end_date": "2024-12-31"
}
```

**Performance Metrics:**
- `total_return`: Total return over period
- `annual_return`: Annualized return
- `volatility`: Annual volatility
- `sharpe_ratio`: Risk-adjusted return (target > 1.0)
- `sortino_ratio`: Downside risk-adjusted return
- `max_drawdown`: Maximum peak-to-trough decline
- `win_rate`: Percentage of profitable trades (target > 55%)
- `profit_factor`: Gross profit / gross loss
- `alpha`: Excess return vs benchmark (target > 5%)
- `beta`: Systematic risk vs market
- `information_ratio`: Active return / tracking error (target > 0.5)

---

### 7. Get Quick Stats

**GET** `/api/backtest/quick-stats/{symbol}`

Get basic statistics for an asset without full backtest.

**Parameters:**
- `symbol` (path): Asset symbol
- `start_date` (query): Start date
- `end_date` (query): End date

**Response:**
```json
{
  "symbol": "SPY",
  "metrics": {
    "total_return": 0.35,
    "annual_return": 0.08,
    "volatility": 0.16,
    "sharpe_ratio": 1.15,
    "max_drawdown": -0.22
  },
  "data_points": 1258
}
```

---

### 8. Analyze Assets

**POST** `/api/analysis/`

Perform comprehensive analysis on multiple assets.

**Request Body:**
```json
{
  "symbols": ["SPY", "TLT", "GLD"],
  "start_date": "2023-01-01",
  "end_date": "2024-12-31",
  "include_correlations": true,
  "include_technical": true
}
```

**Response:**
```json
[
  {
    "symbol": "SPY",
    "statistics": {
      "mean_price": 445.30,
      "current_price": 450.25,
      "min_price": 380.50,
      "max_price": 475.80,
      "volatility": 12.45,
      "total_data_points": 504
    },
    "returns_summary": {
      "mean_return": 0.0008,
      "total_return": 0.18,
      "volatility_annual": 0.16,
      "skewness": -0.35,
      "kurtosis": 3.2
    },
    "correlations": {
      "TLT": -0.25,
      "GLD": 0.15
    },
    "technical_indicators": {
      "rsi": 55.3,
      "macd": 2.45,
      "macd_signal": 2.10,
      "bb_upper": 460.20,
      "bb_middle": 450.25,
      "bb_lower": 440.30,
      "sma_20": 448.60,
      "sma_50": 445.30
    }
  }
]
```

---

### 9. Get Price History

**GET** `/api/analysis/price-history/{symbol}`

Get historical OHLCV data for an asset.

**Parameters:**
- `symbol` (path): Asset symbol
- `start_date` (query): Start date
- `end_date` (query): End date

**Response:**
```json
{
  "symbol": "SPY",
  "data": [
    {
      "date": "2023-01-03",
      "open": 380.50,
      "high": 385.20,
      "low": 379.80,
      "close": 383.45,
      "volume": 75000000
    }
  ],
  "total_points": 504
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Asset or model not found |
| 500 | Internal Server Error - Processing error |

---

## Rate Limiting

Currently no rate limiting. For production, implement rate limiting:
- 100 requests per minute for predictions
- 10 requests per minute for backtests (resource intensive)

---

## Best Practices

1. **Asset Selection**
   - Limit predictions to 5 assets at a time
   - Limit backtests to 3 assets (computational cost)

2. **Date Ranges**
   - Minimum 1 year of historical data for training
   - Use recent data for better predictions

3. **Model Selection**
   - `xgboost`: Best overall performance (recommended)
   - `random_forest`: Good for feature importance
   - `linear`: Fast, interpretable baseline
   - `lstm`: Best for sequential patterns
   - `ensemble`: Combines all models

4. **Caching**
   - Predictions are cached for 1 hour
   - Same parameters will return cached results

---

## Example Workflows

### Workflow 1: Quick Analysis
```bash
# 1. Get available assets
curl http://localhost:8000/api/assets/

# 2. Analyze SPY
curl -X POST http://localhost:8000/api/analysis/ \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["SPY"], "start_date": "2023-01-01", "end_date": "2024-12-31"}'

# 3. Get predictions
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["SPY"], "model_type": "xgboost"}'
```

### Workflow 2: Strategy Backtesting
```bash
# 1. Backtest strategy
curl -X POST http://localhost:8000/api/backtest/ \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": ["SPY", "TLT"],
    "model_type": "xgboost",
    "start_date": "2020-01-01",
    "end_date": "2024-12-31"
  }'

# 2. Get feature importance
curl http://localhost:8000/api/predict/feature-importance/SPY?model_type=xgboost
```

---

## Support

- Interactive API Docs: http://localhost:8000/api/docs
- Alternative Docs: http://localhost:8000/api/redoc
- GitHub: https://github.com/aniktahabilder/market-intelligence-ml
