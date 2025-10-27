# Market Intelligence ML - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                   React + TypeScript + Vite                     │
│                         Port: 3000                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       FastAPI Backend                           │
│                         Port: 8000                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Prediction   │  │  Backtest    │  │  Analysis    │         │
│  │   Service    │  │   Service    │  │   Service    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ML Engine                                  │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌──────────┐      │
│  │ XGBoost  │  │   LSTM    │  │ Random   │  │ Ensemble │      │
│  │          │  │           │  │ Forest   │  │          │      │
│  └──────────┘  └───────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Processing Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Feature     │  │  Technical   │  │  Cross-Asset │         │
│  │ Engineering  │  │  Indicators  │  │  Features    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Sources                                │
│        ┌──────────────┐          ┌──────────────┐              │
│        │  yfinance    │          │    CCXT      │              │
│        │ (Stocks/ETFs)│          │   (Crypto)   │              │
│        └──────────────┘          └──────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite (fast dev server, HMR)
- **Styling**: TailwindCSS (utility-first CSS)
- **Routing**: React Router v6
- **State Management**: TanStack Query (server state), Zustand (client state)
- **Charts**: Recharts (responsive, composable)
- **HTTP Client**: Axios
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI (modern, async Python)
- **Server**: Uvicorn (ASGI server)
- **Validation**: Pydantic v2 (type-safe schemas)
- **ML Libraries**:
  - XGBoost 2.0+ (gradient boosting)
  - TensorFlow 2.13+ (LSTM models)
  - scikit-learn 1.3+ (baseline models)
- **Data Processing**: pandas, NumPy
- **Financial Data**: yfinance (stocks), ccxt (crypto)

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Deployment**: Multi-container orchestration
- **Development**: Hot reload for both frontend/backend

---

## Component Breakdown

### Frontend Components

#### Pages
1. **Dashboard** (`/`)
   - Welcome screen
   - Quick stats
   - Feature overview
   - Getting started guide

2. **Predictions** (`/predictions`)
   - Asset selector (multi-select)
   - Model configuration
   - Prediction results cards
   - Signal indicators (BUY/SELL/HOLD)
   - Confidence scores

3. **Backtest** (`/backtest`)
   - Strategy configuration
   - Date range selector
   - Performance metrics grid
   - Equity curve chart
   - Target metrics comparison

4. **Analysis** (`/analysis`)
   - Multi-asset comparison
   - Technical indicators
   - Correlation matrix
   - Returns/volatility charts

#### Reusable Components
- **Layout**: Navigation, header, footer
- **AssetSelector**: Multi-select with search
- **Charts**: Line, bar, radar (via Recharts)

### Backend Services

#### 1. Prediction Service
**Location**: `backend/app/services/prediction_service.py`

**Responsibilities**:
- Feature engineering (technical indicators)
- Model training (on-demand)
- Return predictions
- Feature importance calculation

**Key Methods**:
- `prepare_features()`: Calculate 80+ indicators
- `train_model()`: Train ML model
- `predict()`: Generate predictions
- `get_feature_importance()`: Extract important features

#### 2. Backtest Service
**Location**: `backend/app/services/backtest_service.py`

**Responsibilities**:
- Walk-forward validation
- Portfolio simulation
- Transaction cost modeling
- Performance metrics calculation

**Key Methods**:
- `run_backtest()`: Execute backtest
- Calculates: Sharpe, Sortino, Alpha, Beta, Max DD, Win Rate

#### 3. API Endpoints

**Assets** (`/api/assets/`):
- `GET /`: List all assets
- `GET /categories`: Assets by category
- `GET /{symbol}`: Asset details

**Predictions** (`/api/predict/`):
- `POST /`: Generate predictions
- `GET /feature-importance/{symbol}`: Feature analysis

**Backtest** (`/api/backtest/`):
- `POST /`: Run backtest
- `GET /quick-stats/{symbol}`: Quick metrics

**Analysis** (`/api/analysis/`):
- `POST /`: Analyze assets
- `GET /price-history/{symbol}`: Historical data

---

## Data Flow

### Prediction Flow
```
1. User selects assets (SPY, BTC/USDT)
           ↓
2. Frontend sends POST /api/predict/
           ↓
3. Backend fetches historical data (yfinance/ccxt)
           ↓
4. Feature engineering (80+ indicators calculated)
           ↓
5. Model training (XGBoost on features)
           ↓
6. Prediction generation (next 1d/5d/20d/60d)
           ↓
7. Response with predictions + confidence
           ↓
8. Frontend displays results + charts
```

### Backtest Flow
```
1. User configures backtest (assets, dates, capital)
           ↓
2. Frontend sends POST /api/backtest/
           ↓
3. Backend trains models on historical data
           ↓
4. Walk-forward simulation:
   - Generate predictions at each timepoint
   - Execute trades based on signals
   - Apply transaction costs
   - Track portfolio value
           ↓
5. Calculate performance metrics
           ↓
6. Response with metrics + equity curve + trades
           ↓
7. Frontend displays charts + metrics grid
```

---

## Feature Engineering Pipeline

### Technical Indicators (per asset)
- **Trend**: SMA (5,10,20,50,200), EMA
- **Momentum**: RSI, MACD, Stochastic
- **Volatility**: Bollinger Bands, ATR
- **Volume**: Volume ratios, OBV

### Cross-Asset Features
- **Correlations**: Rolling correlations between assets
- **Ratios**: Asset price ratios (SPY/TLT, etc.)

### Macro Features
- **VIX**: Volatility regime detection
- **Yield Spreads**: Bond market signals

**Total**: 80+ engineered features

---

## ML Models

### 1. XGBoost (Primary)
- **Type**: Gradient Boosting
- **Use Case**: Best overall performance
- **Features**: Feature importance, handles missing data
- **Hyperparameters**: 100 estimators, depth 5, LR 0.01

### 2. Random Forest
- **Type**: Ensemble (bagging)
- **Use Case**: Feature importance analysis
- **Features**: Interpretable, robust

### 3. Linear Regression
- **Type**: Baseline model
- **Use Case**: Benchmark comparison
- **Features**: Fast, interpretable

### 4. LSTM
- **Type**: Deep Learning (RNN)
- **Use Case**: Sequential patterns
- **Features**: Captures time dependencies

### 5. Ensemble
- **Type**: Meta-model
- **Use Case**: Combines all models
- **Features**: Best predictions from each model

---

## Performance Metrics

### Return Metrics
- **Total Return**: Overall gain/loss
- **Annual Return**: Annualized performance
- **Volatility**: Risk measure (annual std dev)

### Risk-Adjusted Metrics
- **Sharpe Ratio**: Return per unit of risk (target > 1.0)
- **Sortino Ratio**: Return per downside risk
- **Calmar Ratio**: Return / Max Drawdown

### Benchmark-Relative
- **Alpha**: Excess return vs benchmark (target > 5%)
- **Beta**: Systematic risk
- **Information Ratio**: Active return / tracking error (target > 0.5)

### Win/Loss
- **Win Rate**: % profitable trades (target > 55%)
- **Profit Factor**: Gross profit / Gross loss
- **Max Drawdown**: Peak-to-trough decline (target < 25%)

---

## Security Considerations

### Current Implementation
- No authentication (open API)
- CORS enabled for localhost
- No rate limiting

### Production Recommendations
1. **Authentication**: Implement JWT tokens
2. **Rate Limiting**: Prevent abuse
   - 100 req/min for predictions
   - 10 req/min for backtests
3. **HTTPS**: Enable SSL/TLS
4. **Input Validation**: Already implemented via Pydantic
5. **CORS**: Restrict to production domains

---

## Scalability

### Current Limitations
- Single-process (no multi-worker)
- No caching layer (Redis)
- No database (file-based storage)

### Scaling Strategy
1. **Horizontal Scaling**:
   - Multiple uvicorn workers
   - Load balancer (nginx)

2. **Caching**:
   - Redis for predictions
   - Cache invalidation on data updates

3. **Database**:
   - PostgreSQL for persistent storage
   - Store predictions, backtest results

4. **Async Processing**:
   - Celery for long-running tasks
   - Background job queue for backtests

---

## Deployment

### Development
```bash
docker-compose up
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables
- `ALLOWED_ORIGINS`: CORS domains
- `DEFAULT_MODEL`: Default ML model
- `CACHE_TTL`: Prediction cache duration
- `VITE_API_URL`: Frontend API endpoint

---

## Monitoring & Logging

### Current Implementation
- FastAPI automatic logging
- Console output

### Production Recommendations
1. **Logging**: Structured logging (JSON)
2. **Metrics**: Prometheus + Grafana
3. **Error Tracking**: Sentry
4. **Performance**: APM (New Relic, DataDog)

---

## Testing Strategy

### Unit Tests
- Model predictions
- Feature engineering
- Metric calculations

### Integration Tests
- API endpoint responses
- End-to-end workflows

### Load Tests
- Concurrent predictions
- Backtest performance

---

## Future Enhancements

1. **Real-time Predictions**: WebSocket streaming
2. **User Accounts**: Authentication & saved strategies
3. **Alerting**: Email/SMS for signals
4. **More Models**: Transformer models, Prophet
5. **Options Trading**: Greeks calculation, volatility surface
6. **Portfolio Optimization**: MPT, Black-Litterman
7. **Sentiment Analysis**: News, social media

---

## Documentation

- **Setup Guide**: [SETUP.md](SETUP.md)
- **API Reference**: [API_GUIDE.md](API_GUIDE.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **README**: [README.md](README.md)
