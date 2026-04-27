# Quick Start Guide

## 🎯 Getting Started in 5 Minutes

### Option 1: Automatic Setup (Recommended)

#### macOS/Linux:
```bash
chmod +x setup.sh
./setup.sh
```

#### Windows:
```bash
setup.bat
```

### Option 2: Manual Setup

#### 1. Install Python Dependencies

```bash
cd backend
python -m venv venv

# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate.bat

pip install -r requirements.txt
```

#### 2. Start Backend Server

```bash
python run.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

#### 3. Start Frontend

In a new terminal:

```bash
cd frontend

# Option A: Use Python's built-in server
python -m http.server 8000

# Option B: Use node/npm if installed
npx http-server

# Option C: Open directly in browser
open index.html  # macOS
# or just double-click index.html
```

Then visit: **http://localhost:8000** (or http://localhost:3000 if using http-server)

---

## 📊 Testing the Application

### Test Stock Analysis

1. Go to **Dashboard** tab
2. You should see trending stocks loading
3. Go to **Analyzer** tab
4. Enter "AAPL" in the stock symbol field
5. Click "Analyze"
6. Review the technical indicators and signals

### Test Exit Strategy

1. Go to **Exit Strategy Planner** tab
2. Enter Entry Price: `150.00`
3. Enter Current Price: `155.00`
4. Enter Quantity: `100`
5. Enter Capital: `15000`
6. Click "Generate Exit Plan"
7. Review the exit points and strategies

### Test Stock Screener

1. Go to **Dashboard** 
2. Scroll down to see screened stocks
3. View results sorted by signal strength

### Test Portfolio

1. Go to **Portfolio** tab
2. Under "Buy Stocks", enter:
   - Symbol: `AAPL`
   - Quantity: `10`
3. Click "Buy"
4. Check your portfolio in the table below
5. Test selling by entering symbol and quantity

---

## 🔧 Configuration

Edit `backend/config.py` to customize:

```python
# Trading parameters
SHORT_MA_WINDOW = 20          # Adjust for faster/slower signals
LONG_MA_WINDOW = 50           # Long-term trend
STOP_LOSS_PERCENT = 0.05      # 5% stop loss
TAKE_PROFIT_TARGETS = [0.25, 0.50, 1.0, 2.0, 4.0]  # 1x-4x returns

# Data settings
DATA_PERIOD = "1y"            # How much historical data
INTERVAL = "1d"               # Daily candles
```

---

## 📱 API Endpoints Reference

### Analyze Stock
```bash
curl -X POST http://localhost:5000/api/stock/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "period": "1y", "interval": "1d"}'
```

### Get Exit Plan
```bash
curl -X POST http://localhost:5000/api/stock/exit-plan \
  -H "Content-Type: application/json" \
  -d '{
    "entry_price": 150,
    "current_price": 155,
    "quantity": 100,
    "capital_allocated": 15000
  }'
```

### Stock Screener
```bash
curl http://localhost:5000/api/stock/screener
```

### Trending Stocks
```bash
curl http://localhost:5000/api/stock/trending
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Address already in use"
The port 5000 is already taken. Either:
- Kill the process: `lsof -ti:5000 | xargs kill -9`
- Or change port in `run.py`

### Issue: Frontend not connecting to API
Check that:
1. Backend is running on `http://localhost:5000`
2. CORS is enabled (it should be by default)
3. Check browser console for errors (F12)

### Issue: No stock data showing
This requires internet connection to fetch data from Yahoo Finance. Check:
1. Internet connection is active
2. Firewall isn't blocking yfinance
3. Yahoo Finance API isn't being rate-limited

---

## 📈 Trading Workflow

### Step 1: Screen for Opportunities
- View Dashboard screener
- Look for STRONG_BUY signals
- Check momentum values

### Step 2: Analyze Deeply
- Go to Analyzer
- Enter stock symbol
- Review all technical indicators
- Confirm the signal

### Step 3: Plan Exit
- Go to Exit Strategy Planner
- Enter your planned entry price
- Review exit targets and stop loss
- Plan pyramiding/scaling strategy

### Step 4: Execute (Simulation)
- Go to Portfolio
- Simulate buying the stock
- Monitor it on dashboard

### Step 5: Manage Position
- Watch for exit signals
- Follow your exit plan
- Lock in profits at targets
- Cut losses at stop loss

---

## 💡 Trading Tips

1. **Follow the Signals**: Let the algorithm guide you
2. **Respect Stop Loss**: Always use it, discipline is key
3. **Scale Progressively**: Use pyramiding, not all-in
4. **Take Profits**: Use scaling strategy, don't get greedy
5. **Diversify**: Don't put everything in one stock
6. **Test First**: Paper trade before real money
7. **Keep Records**: Track all trades for learning

---

## 🚀 Next Steps

### To Deploy to Production:

1. **Change SECRET_KEY** in `backend/config.py`
2. **Set FLASK_ENV=production**
3. **Use a production WSGI server** (Gunicorn, uWSGI)
4. **Add SSL/HTTPS** with nginx/Apache
5. **Set up database** (PostgreSQL, MongoDB)
6. **Enable user authentication**
7. **Add broker API integration** (Alpaca, Interactive Brokers)

### For Real Trading:

1. Open account with broker (Alpaca, TD Ameritrade, etc.)
2. Get API credentials
3. Integrate broker API into backend
4. Test thoroughly with paper trading first
5. Start with small positions
6. Scale up gradually

---

## 📚 Learning Resources

- **Technical Analysis**: investopedia.com
- **Python Finance**: python-finance.readthedocs.io
- **yfinance**: github.com/ranaroussi/yfinance
- **TA-Lib**: ta-lib.org

---

## 📞 Support

For issues:
1. Check the README.md
2. Review the code comments
3. Check the browser console (F12)
4. Check Flask console output

---

Happy Trading! 📈

Remember: Education first, then paper trading, then real trading with small sizes.
