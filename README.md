# Market Intelligence ML

**Multi-Asset Predictive Modeling for Equities, Fixed Income & Digital Assets**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)]()

---

## 🎯 Overview

Market Intelligence ML is an end-to-end machine learning framework for quantitative market analysis and alpha signal generation. The system applies supervised learning, time-series forecasting, and ensemble methods to predict returns across multiple asset classes.

**Key Features:**
- 📊 Multi-asset forecasting (equities, bonds, commodities, crypto)
- 🤖 Ensemble learning (XGBoost, LSTM, Random Forest)
- 📈 80+ engineered features (technical, cross-asset, macro)
- 🎲 Market regime detection
- �� Comprehensive backtesting with transaction costs
- 📊 Risk-adjusted performance metrics

---

## ��️ Project Structure
```
market-intelligence-ml/
├── configs/              # Configuration files
├── data/                 # Data storage
│   ├── raw/             # Raw market data
│   ├── processed/       # Cleaned data
│   ├── features/        # Engineered features
│   └── results/         # Intermediate results
├── notebooks/           # Jupyter notebooks (5 total)
├── src/                 # Source code
│   ├── data/           # Data fetching & preprocessing
│   ├── features/       # Feature engineering
│   ├── models/         # ML models
│   ├── backtest/       # Backtesting framework
│   └── utils/          # Utilities
├── results/            # Final outputs
│   ├── plots/         # Visualizations
│   ├── reports/       # Analysis reports
│   └── models/        # Trained models
└── tests/             # Unit tests
```

---

## 🚀 Quick Start

### Option A: Full-Stack Web Application (Recommended)

**Using Docker (Easiest):**
```bash
git clone https://github.com/aniktahabilder/market-intelligence-ml.git
cd market-intelligence-ml

# Start both frontend and backend
docker-compose up --build

# Access the app
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

**Manual Setup:**
```bash
# Backend
source venv/bin/activate
pip install -r requirements.txt -r backend/requirements.txt
cd backend && uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

See [SETUP.md](SETUP.md) for detailed instructions.

### Option B: Jupyter Notebooks (Research)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook

# Run notebooks in order:
# 01_data_exploration.ipynb
# 02_feature_engineering.ipynb
# 03_baseline_models.ipynb
# 04_advanced_models.ipynb
# 05_ensemble_backtesting.ipynb
```

---

## 📊 Asset Universe

**15 Assets across 4 Classes:**

| Category | Assets | Purpose |
|----------|--------|---------|
| **Equities** | SPY, XLK, XLF, XLV, XLE, XLI | Market + sectors |
| **Fixed Income** | TLT, IEF | Duration diversification |
| **Alternatives** | GLD, BTC, ETH, SOL | Uncorrelated returns |
| **Macro** | VIX | Volatility indicator |

---

## 🔧 Methodology

**Feature Engineering:**
- Technical indicators (RSI, MACD, Bollinger Bands, MAs)
- Cross-asset signals (correlations, ratios)
- Macro factors (VIX, yield spreads, Fed Funds Rate)

**Models:**
1. Linear Regression (baseline)
2. Random Forest (feature importance)
3. XGBoost (primary model)
4. LSTM (sequential patterns)
5. Ensemble (meta-model)

**Backtesting:**
- Walk-forward validation
- Transaction costs (10 bps)
- Realistic slippage
- Out-of-sample testing

---

## 📈 Target Metrics

| Metric | Target |
|--------|--------|
| **Directional Accuracy** | > 55% |
| **Information Ratio** | > 0.5 |
| **Annualized Alpha** | > 5% |
| **Max Drawdown** | < 25% |
| **Sharpe Ratio** | > 1.0 |

---

## 🔗 Related Projects

This is part of a three-project portfolio:

1. **Market Intelligence ML** ← *You are here*
2. [FinRisk Analytics](https://github.com/aniktahabilder/finrisk-analytics) - Risk modeling
3. [AlphaRL Portfolio](https://github.com/aniktahabilder/alpharl-portfolio) - RL optimization

---

## 📚 Dependencies

**Backend:**
- Python 3.9+
- FastAPI, uvicorn
- pandas, numpy, scipy
- scikit-learn, xgboost, tensorflow
- yfinance, ccxt (data sources)

**Frontend:**
- Node.js 18+
- React 18, TypeScript
- Vite, TailwindCSS
- Recharts (visualizations)
- Axios, TanStack Query

See `requirements.txt`, `backend/requirements.txt`, and `frontend/package.json`.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

## 👤 Author

**Anik Tahabilder**
- PhD Student, Computer Science, Wayne State University
- GitHub: [@aniktahabilder](https://github.com/aniktahabilder)

---

## 🛠️ Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

**Notebooks (Research):**
```bash
make test       # Run tests
make format     # Format code
make notebook   # Launch notebooks
```

**Web Application:**
```bash
# Backend development
cd backend
uvicorn app.main:app --reload

# Frontend development
cd frontend
npm run dev

# Run tests
pytest backend/tests/
npm run test --prefix frontend
```

**API Documentation:**
- Interactive: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- Guide: [API_GUIDE.md](API_GUIDE.md)

## 📞 Contact

For questions or collaboration:
- GitHub: [aniktahabilder](https://github.com/aniktahabilder)
- Email: [your-email]

---

## 🙏 Acknowledgments

- Financial data provided by Yahoo Finance and CCXT
- Built with scikit-learn, XGBoost, and TensorFlow
- Inspired by academic research in quantitative finance

---

**⭐ Star this repo if you find it useful!**
