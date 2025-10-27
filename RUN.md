# How to Run the Full Project

## ✅ **CURRENTLY RUNNING**

Both frontend and backend are already running:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000

Just open your browser and go to: **http://localhost:3000**

---

## 🔄 **If You Need to Restart**

### **Option 1: Quick Restart (Both Together)**

```bash
# From project root directory
cd /home/anik/code/market-intelligence-ml

# Terminal 1 - Backend
source venv/bin/activate
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend (open new terminal)
cd /home/anik/code/market-intelligence-ml/frontend
npm run dev
```

### **Option 2: Background Mode (Like Now)**

```bash
# Stop existing processes (if needed)
kill $(lsof -ti:8000)  # Stop backend
kill $(lsof -ti:3000)  # Stop frontend

# Start backend in background
source venv/bin/activate
cd backend
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &

# Start frontend in background
cd ../frontend
npm run dev > frontend.log 2>&1 &
```

---

## 📍 **Important URLs**

- **Frontend (Main App)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **API Alternative Docs**: http://localhost:8000/api/redoc

---

## ✨ **First Time Usage**

1. **Open Browser**: http://localhost:3000

2. **Dashboard** - You'll see:
   - Welcome message
   - Stats (15 available assets, 5 ML models, 80+ features)
   - Feature cards

3. **Make Your First Prediction**:
   - Click "Predictions" in navigation
   - Select 1-2 assets (e.g., SPY)
   - Model: XGBoost
   - Horizon: 1 Day
   - Click "Generate Predictions"
   - **Wait 30-60 seconds** (first time trains the model)

4. **View Results**:
   - Predicted return percentage
   - BUY/SELL/HOLD signal
   - Confidence score
   - Target price

---

## 🛑 **Stop the Application**

```bash
# Stop backend
kill $(lsof -ti:8000)

# Stop frontend
kill $(lsof -ti:3000)

# Or stop all node/python processes (careful!)
pkill -f uvicorn
pkill -f vite
```

---

## 📊 **Check Status**

```bash
# Check if backend is running
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

# Check if frontend is running
curl -I http://localhost:3000
# Should return: HTTP/1.1 200 OK

# View running processes
ps aux | grep -E "uvicorn|vite" | grep -v grep
```

---

## 📝 **View Logs**

```bash
# Backend logs
tail -f backend/backend.log

# Frontend logs
tail -f frontend/frontend.log
```

---

## 🎯 **What You Can Do**

### 1. Predictions Page
- Select up to 5 assets
- Choose ML model (XGBoost, LSTM, Random Forest, Linear, Ensemble)
- Select prediction horizon (1d, 5d, 20d, 60d)
- Get predictions with confidence scores
- See BUY/SELL/HOLD signals

### 2. Backtest Page
- Test trading strategies
- Configure: assets, dates, initial capital
- View performance metrics:
  - Sharpe Ratio, Win Rate, Max Drawdown
  - Total Return, Annual Return
  - Alpha, Beta, Information Ratio
- Interactive equity curve chart

### 3. Analysis Page
- Compare multiple assets
- View technical indicators (RSI, MACD, Bollinger Bands)
- Correlation matrix
- Returns and volatility comparison charts

---

## 🐛 **Troubleshooting**

### Backend won't start
```bash
# Check port 8000 is free
lsof -i :8000

# If occupied, kill it
kill $(lsof -ti:8000)

# Check Python dependencies
source venv/bin/activate
pip list | grep fastapi
```

### Frontend won't start
```bash
# Check port 3000 is free
lsof -i :3000

# If occupied, kill it
kill $(lsof -ti:3000)

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Can't connect to backend
```bash
# Check if backend is actually running
curl http://localhost:8000/health

# Check frontend .env file
cat frontend/.env
# Should contain: VITE_API_URL=http://localhost:8000
```

---

## 📚 **Documentation**

- **Setup Guide**: SETUP.md
- **API Reference**: API_GUIDE.md
- **Architecture**: ARCHITECTURE.md
- **Quick Start**: QUICKSTART.md

---

**Enjoy your ML trading platform! 🚀📈**
