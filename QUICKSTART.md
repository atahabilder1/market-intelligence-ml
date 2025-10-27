# Market Intelligence ML - Quick Start Guide

Get up and running in 5 minutes!

---

## 🚀 Fastest Way to Run

### Using Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/aniktahabilder/market-intelligence-ml.git
cd market-intelligence-ml

# 2. Start everything with one command
docker-compose up --build

# 3. Wait for services to start (1-2 minutes)
# You'll see: "Application startup complete"

# 4. Open your browser
```

**Access the application:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

That's it! You're ready to use the application.

---

## 📱 Using the Application

### 1. Make Your First Prediction

1. Go to http://localhost:3000
2. Click **"Predictions"** in the navigation
3. Select assets (e.g., SPY, BTC/USDT)
4. Choose model: **XGBoost** (recommended)
5. Click **"Generate Predictions"**

**Result**: You'll see predicted returns, confidence scores, and BUY/SELL/HOLD signals.

### 2. Run a Backtest

1. Click **"Backtest"**
2. Select 1-3 assets
3. Set date range (e.g., 2020-01-01 to 2024-12-31)
4. Click **"Run Backtest"**

**Result**: Performance metrics (Sharpe ratio, returns, drawdown) and equity curve chart.

### 3. Analyze Assets

1. Click **"Analysis"**
2. Select multiple assets to compare
3. Click **"Run Analysis"**

**Result**: Correlations, technical indicators, returns comparison.

---

## 🛠️ Manual Setup (Without Docker)

### Backend

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt

# 3. Start backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend running at: http://localhost:8000

### Frontend

```bash
# Open a new terminal

# 1. Install Node.js dependencies
cd frontend
npm install

# 2. Start frontend
npm run dev
```

Frontend running at: http://localhost:3000

---

## 📊 What Can You Do?

### Price Predictions
- **Input**: Select assets (SPY, BTC, ETH, etc.)
- **Output**:
  - Predicted return (e.g., +2.5%)
  - Confidence score (0-100%)
  - Trading signal (BUY/SELL/HOLD)
  - Target price

### Backtesting
- **Input**: Strategy configuration
- **Output**:
  - Performance metrics (Sharpe, Win Rate, Alpha)
  - Equity curve chart
  - Trade history
  - Comparison vs targets

### Analysis
- **Input**: Multiple assets
- **Output**:
  - Technical indicators (RSI, MACD, Bollinger Bands)
  - Correlation matrix
  - Returns & volatility comparison
  - Statistical summary

---

## 💡 Example Workflows

### Workflow 1: "Should I buy SPY today?"

1. Go to **Predictions** page
2. Select **SPY**
3. Model: **XGBoost**, Horizon: **1 Day**
4. Click **Generate Predictions**

**Interpretation**:
- Green BUY signal + high confidence → Consider buying
- Red SELL signal + high confidence → Consider selling
- Yellow HOLD → Wait for better signal

### Workflow 2: "Test a trading strategy"

1. Go to **Backtest** page
2. Select assets: **SPY, TLT** (60/40 portfolio)
3. Date: **2020-01-01** to **2024-12-31**
4. Capital: **$100,000**
5. Click **Run Backtest**

**Metrics to check**:
- ✅ Sharpe Ratio > 1.0 → Good risk-adjusted returns
- ✅ Win Rate > 55% → More wins than losses
- ✅ Max Drawdown < 25% → Acceptable risk

### Workflow 3: "Compare crypto vs stocks"

1. Go to **Analysis** page
2. Select: **SPY, BTC/USDT, ETH/USDT**
3. Date: Last 2 years
4. Click **Run Analysis**

**What to look for**:
- Correlation matrix → Diversification benefits
- Returns comparison → Performance leaders
- Volatility → Risk assessment

---

## 🎓 Understanding the Models

### XGBoost (Recommended)
- **Best for**: Overall accuracy
- **Speed**: Fast
- **Accuracy**: Highest
- **Use when**: General predictions

### Random Forest
- **Best for**: Feature importance analysis
- **Speed**: Medium
- **Accuracy**: Good
- **Use when**: Want to understand which indicators matter

### Linear Regression
- **Best for**: Simple baseline
- **Speed**: Very fast
- **Accuracy**: Baseline
- **Use when**: Quick rough estimates

### LSTM
- **Best for**: Sequential patterns
- **Speed**: Slower
- **Accuracy**: Good for time series
- **Use when**: Analyzing trends over time

### Ensemble
- **Best for**: Maximum accuracy
- **Speed**: Slowest (uses all models)
- **Accuracy**: Best
- **Use when**: Final decision, not prototyping

---

## 📈 Available Assets

### Equities (6)
- **SPY**: S&P 500
- **XLK**: Technology
- **XLF**: Financials
- **XLV**: Healthcare
- **XLE**: Energy
- **XLI**: Industrials

### Fixed Income (2)
- **TLT**: 20+ Year Treasury Bonds
- **IEF**: 7-10 Year Treasury Bonds

### Commodities (1)
- **GLD**: Gold ETF

### Crypto (3)
- **BTC/USDT**: Bitcoin
- **ETH/USDT**: Ethereum
- **SOL/USDT**: Solana

### Macro (1)
- **^VIX**: Volatility Index

**Total**: 13 assets across 4 classes

---

## 🔧 Common Issues

### "Cannot connect to backend"
**Solution**: Make sure backend is running at http://localhost:8000

```bash
# Check if backend is running
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

### "Port already in use"
**Backend (8000)**:
```bash
# Find what's using port 8000
lsof -i :8000
# Kill it
kill -9 <PID>
```

**Frontend (3000)**:
```bash
# Change port in frontend/vite.config.ts
server: { port: 3001 }
```

### "No data available"
**Cause**: Internet connection required for data fetching

**Solution**:
- Check internet connection
- yfinance and ccxt download data from external sources

### "Prediction taking too long"
**Cause**: First prediction trains the model (30-60 seconds)

**Solution**:
- Wait for training to complete
- Subsequent predictions will be faster (cached model)

---

## 📚 Next Steps

1. **Read Documentation**:
   - [SETUP.md](SETUP.md) - Detailed setup
   - [API_GUIDE.md](API_GUIDE.md) - API reference
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design

2. **Try the Notebooks**:
   ```bash
   jupyter notebook notebooks/
   ```
   - Run notebooks 01-05 to understand the ML pipeline

3. **Customize**:
   - Edit `configs/config.yaml` for different assets
   - Modify model parameters in backend code
   - Add new features in `src/features/`

4. **Deploy**:
   - Production deployment guide in SETUP.md
   - Use docker-compose for easy deployment

---

## 🆘 Getting Help

- **Documentation**: Read SETUP.md and API_GUIDE.md
- **API Docs**: http://localhost:8000/api/docs (interactive)
- **Issues**: https://github.com/aniktahabilder/market-intelligence-ml/issues
- **Contributing**: See CONTRIBUTING.md

---

## 🎯 Target Performance Metrics

When backtesting, aim for these targets:

| Metric | Target | Meaning |
|--------|--------|---------|
| Sharpe Ratio | > 1.0 | Good risk-adjusted returns |
| Win Rate | > 55% | More than half trades profitable |
| Annual Alpha | > 5% | Beat benchmark by 5% |
| Max Drawdown | < 25% | Acceptable risk |
| Information Ratio | > 0.5 | Consistent outperformance |

---

**Happy Trading! 📈**

---

*Disclaimer: This is for educational purposes only. Not financial advice. Past performance doesn't guarantee future results.*
