# Market Intelligence ML - Setup Guide

Complete setup instructions for the full-stack application.

---

## Architecture Overview

```
┌─────────────────┐      HTTP/REST      ┌──────────────────┐
│  React Frontend │ ◄─────────────────► │  FastAPI Backend │
│   (Port 3000)   │                      │   (Port 8000)    │
└─────────────────┘                      └──────────────────┘
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │   ML Models     │
                                         │  (XGBoost,LSTM) │
                                         └─────────────────┘
```

---

## Quick Start (Docker - Recommended)

### Prerequisites
- Docker & Docker Compose
- Git

### Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/aniktahabilder/market-intelligence-ml.git
   cd market-intelligence-ml
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   cp frontend/.env.example frontend/.env
   ```

3. **Start Services**
   ```bash
   docker-compose up --build
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs

---

## Manual Setup (Development)

### Backend Setup

1. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r backend/requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Start Backend**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at: http://localhost:8000

### Frontend Setup

1. **Install Node.js Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Ensure VITE_API_URL=http://localhost:8000
   ```

3. **Start Frontend**
   ```bash
   npm run dev
   ```

   Frontend will be available at: http://localhost:3000

---

## Project Structure

```
market-intelligence-ml/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── models/         # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API client
│   │   └── types/         # TypeScript types
│   ├── package.json
│   └── Dockerfile
├── src/                    # Original ML Code
│   ├── data/              # Data fetching
│   ├── features/          # Feature engineering
│   ├── models/            # ML models
│   └── backtest/          # Backtesting
├── notebooks/             # Jupyter notebooks
├── configs/               # Configuration files
├── data/                  # Data storage
├── results/               # Model outputs
└── docker-compose.yml
```

---

## API Endpoints

### Assets
- `GET /api/assets/` - List all available assets
- `GET /api/assets/categories` - Get assets by category
- `GET /api/assets/{symbol}` - Get asset details

### Predictions
- `POST /api/predict/` - Generate predictions
- `GET /api/predict/feature-importance/{symbol}` - Get feature importance

### Backtesting
- `POST /api/backtest/` - Run backtest
- `GET /api/backtest/quick-stats/{symbol}` - Get quick statistics

### Analysis
- `POST /api/analysis/` - Analyze assets
- `GET /api/analysis/price-history/{symbol}` - Get price history

Full API documentation: http://localhost:8000/api/docs

---

## Usage Examples

### 1. Get Predictions

**Frontend:**
Navigate to "Predictions" page, select assets (e.g., SPY, BTC/USDT), choose model, click "Generate Predictions"

**API (curl):**
```bash
curl -X POST "http://localhost:8000/api/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": ["SPY", "BTC/USDT"],
    "model_type": "xgboost",
    "horizon": "1d"
  }'
```

### 2. Run Backtest

**Frontend:**
Navigate to "Backtest" page, select assets, set date range, click "Run Backtest"

**API (curl):**
```bash
curl -X POST "http://localhost:8000/api/backtest/" \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": ["SPY"],
    "model_type": "xgboost",
    "start_date": "2020-01-01",
    "end_date": "2024-12-31",
    "initial_capital": 100000
  }'
```

### 3. Analyze Assets

**Frontend:**
Navigate to "Analysis" page, select multiple assets, click "Run Analysis"

**API (curl):**
```bash
curl -X POST "http://localhost:8000/api/analysis/" \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": ["SPY", "TLT", "GLD"],
    "start_date": "2023-01-01",
    "end_date": "2024-12-31",
    "include_correlations": true,
    "include_technical": true
  }'
```

---

## Configuration

### Backend (`backend/app/core/config.py`)
- `ALLOWED_ORIGINS`: CORS allowed origins
- `DEFAULT_MODEL`: Default ML model (xgboost)
- `CACHE_PREDICTIONS`: Enable prediction caching
- `DATA_DIR`: Data storage directory

### Frontend (`frontend/src/services/api.ts`)
- `API_BASE_URL`: Backend API URL
- Default: http://localhost:8000

---

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>
```

**Module import errors:**
```bash
# Ensure you're in venv and installed all dependencies
pip install -r requirements.txt -r backend/requirements.txt
```

**Data fetching errors:**
```bash
# Check internet connection
# yfinance and ccxt require internet access
```

### Frontend Issues

**Port 3000 in use:**
```bash
# Change port in frontend/vite.config.ts
server: {
  port: 3001,
}
```

**API connection refused:**
```bash
# Ensure backend is running
# Check VITE_API_URL in frontend/.env
```

**Dependencies not found:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## Development Tips

### Backend Development
- API auto-reloads on code changes (--reload flag)
- Access interactive docs at /api/docs
- Add breakpoints using `import pdb; pdb.set_trace()`

### Frontend Development
- Hot module replacement enabled
- React DevTools recommended
- TypeScript for type safety

### Testing
```bash
# Backend tests
pytest tests/ -v

# Frontend tests (if configured)
cd frontend
npm run test
```

---

## Production Deployment

### Docker Production Build

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Run services
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Production Setup

**Backend:**
```bash
pip install gunicorn
gunicorn backend.app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve dist/ with nginx or similar
```

---

## Support

- GitHub Issues: https://github.com/aniktahabilder/market-intelligence-ml/issues
- Documentation: README.md
- API Docs: http://localhost:8000/api/docs

---

## License

MIT License - see LICENSE file
