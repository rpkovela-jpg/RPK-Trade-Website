# RPK Algorithmic Trading System

A comprehensive algorithmic trading application with Python backend and web-based interface for identifying stocks with 1x-4x+ return potential and planning exit strategies.

## Features

### 📊 Stock Analysis
- **Technical Indicators**: SMA, RSI, MACD, Bollinger Bands, ATR
- **Signal Generation**: Combined signals from multiple indicators
- **Momentum Analysis**: RSI momentum and price momentum tracking
- **Stock Information**: Real-time price, sector, PE ratio, 52-week highs/lows

### 📈 Trading Signals
- **STRONG_BUY / BUY / WEAK_BUY**: High probability entry signals
- **NEUTRAL**: Consolidation phase
- **WEAK_SELL / SELL / STRONG_SELL**: Exit signals
- **Signal Confidence**: Based on multiple indicator agreement

### 🎯 Exit Strategy Planning
- **Take Profit Targets**: 1x, 2x, 4x+ return levels
- **Stop Loss Management**: Automatic 5% stop loss
- **Pyramiding Strategy**: Scale in with multiple tranches
- **Scaling Out Strategy**: Sell portions at each profit target
- **Trailing Stop**: Dynamic stop loss following price up
- **Risk Management**: Capital allocation and position sizing

### 🔍 Stock Screener
- **Pre-built Watchlist**: Monitor popular stocks
- **Signal Strength**: Identify strongest buy/sell signals
- **Momentum Filter**: Sort by momentum strength
- **High Potential**: Focus on 1x-4x+ return opportunities

### 💼 Portfolio Management
- **Buy/Sell Simulation**: Test trading strategies
- **Position Tracking**: Monitor average entry prices
- **P/L Calculation**: Track profits and losses
- **Transaction History**: View all trading activity

## Project Structure

```
RPK Stock/
├── backend/
│   ├── app/
│   │   ├── __init__.py           # Flask app factory
│   │   ├── routes.py             # API endpoints
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── stock_data.py     # Stock data fetching
│   │   └── strategies/
│   │       ├── __init__.py
│   │       ├── analysis.py       # Technical analysis
│   │       ├── signals.py        # Trading signals
│   │       └── exit_strategy.py  # Exit planning
│   ├── config.py                 # Configuration settings
│   ├── run.py                    # Entry point
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # Environment variables
│
└── frontend/
    ├── index.html                # Main HTML
    ├── css/
    │   └── style.css             # Styling
    └── js/
        └── app.js                # Frontend logic
```

## Installation

### Prerequisites
- Python 3.8+
- Node.js/npm (optional, for development)
- Git

### Backend Setup

1. **Install Python dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure environment** (optional):
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Run the server**:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Open in browser**:
For full functionality (including API calls), serve the frontend with a simple HTTP server (recommended), as opening `frontend/index.html` directly in your browser may cause issues with API requests due to browser CORS restrictions:

```bash
cd frontend
python -m http.server 8000
# Then visit http://localhost:8000
```

## API Endpoints

### Stock Analysis
```
POST /api/stock/analyze
Body: { "symbol": "AAPL", "period": "1y", "interval": "1d" }
Response: Technical indicators, signals, momentum, stock info
```

### Exit Strategy Planning
```
POST /api/stock/exit-plan
Body: {
  "entry_price": 150.00,
  "current_price": 155.00,
  "quantity": 100,
  "capital_allocated": 15000
}
Response: Exit points, pyramiding, scaling, risk management
```

### Stock Comparison
```
POST /api/stock/compare
Body: { "symbols": ["AAPL", "GOOGL", "MSFT"] }
Response: Comparative analysis of multiple stocks
```

### Stock Screener
```
GET /api/stock/screener
Response: Pre-screened stocks sorted by potential
```

### Trending Stocks
```
GET /api/stock/trending
Response: Current trending stocks with signals
```

## Trading Strategy Configuration

Edit `backend/config.py` to customize:

```python
SHORT_MA_WINDOW = 20           # Short-term moving average
LONG_MA_WINDOW = 50            # Long-term moving average
RSI_PERIOD = 14                # RSI period
STOP_LOSS_PERCENT = 0.05       # 5% stop loss
TAKE_PROFIT_TARGETS = [0.25, 0.50, 1.0, 2.0, 4.0]  # Profit targets
```

## How to Use

### 1. Analyze a Stock
- Enter stock symbol (e.g., AAPL)
- Select time period
- Click "Analyze"
- Review technical indicators and signals

### 2. Plan Exit Strategy
- Enter entry price
- Enter current price
- Enter quantity and capital
- Click "Generate Exit Plan"
- Review pyramiding and scaling strategies

### 3. Screen for Opportunities
- View screener results on dashboard
- Filter by signal strength
- Monitor momentum indicators

### 4. Manage Portfolio (Simulation)
- Simulate buying/selling stocks
- Track portfolio performance
- Monitor P/L in real-time

## Technical Indicators Explained

### SMA (Simple Moving Average)
- SMA 20: 20-day average (trend direction)
- SMA 50: 50-day average (long-term trend)
- **Signal**: When SMA 20 > SMA 50 = Uptrend (BUY)

### RSI (Relative Strength Index)
- Range: 0-100
- **Below 30**: Oversold (potential BUY)
- **Above 70**: Overbought (potential SELL)
- **30-70**: Neutral

### MACD (Moving Average Convergence Divergence)
- **MACD > Signal Line**: Bullish (BUY)
- **MACD < Signal Line**: Bearish (SELL)

### Bollinger Bands
- **Price < Lower Band**: Oversold (BUY)
- **Price > Upper Band**: Overbought (SELL)
- **Inside Bands**: Normal trading range

### ATR (Average True Range)
- Measures volatility
- Used for dynamic stop loss and position sizing

## Exit Strategy Guide

### Stop Loss
- **Default**: 5% below entry price
- **Purpose**: Limit losses
- **Adjustment**: Can be tightened to 3% for aggressive stops

### Take Profit Targets
```
1x Return    = Entry Price × 1.00 (Break-even to 100% gain)
2x Return    = Entry Price × 2.00 (100% gain)
4x Return    = Entry Price × 4.00 (300% gain)
```

### Pyramiding
- Enter in 4 tranches at different price levels
- Reduces average entry price
- Risk-controlled accumulation

### Scaling Out
- Sell 25% at each 1x, 2x, 4x target
- Lock in profits progressively
- Reduce risk as targets are hit

### Trailing Stop
- Stop loss follows price upward
- Locks in profits
- Prevents giving back gains

## Risk Management Rules

1. **Max Risk Per Trade**: 2% of total capital
2. **Position Sizing**: Based on stop loss distance
3. **Risk-Reward Ratio**: Minimum 1.5:1
4. **Portfolio Diversification**: Don't put all capital in one stock
5. **Exit Discipline**: Follow the exit plan religiously

## Performance Tips

1. **Use Daily Data**: Reduces noise vs. intraday
2. **Combine Signals**: Multiple indicators > single indicator
3. **Follow the Trend**: Trade with the trend, not against it
4. **Manage Risk**: Strict stop losses
5. **Keep Records**: Track all trades

## Disclaimer

⚠️ **IMPORTANT**: This application is for educational and analysis purposes only. It is NOT financial advice. Always:

- Do your own research (DYOR)
- Consult with a financial advisor
- Test strategies in paper trading first
- Start with small position sizes
- Understand your risk tolerance

Stock trading involves significant risk of loss. Past performance does not guarantee future results.

## Technologies Used

### Backend
- **Flask**: Web framework
- **yfinance**: Stock data (Yahoo Finance API)
- **pandas**: Data manipulation
- **TA-Lib**: Technical analysis
- **NumPy**: Numerical computing

### Frontend
- **Bootstrap 5**: UI framework
- **jQuery**: JavaScript library
- **Chart.js**: Data visualization
- **HTML5/CSS3**: Web technologies

## Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and accounts
- [ ] Real broker API integration (Interactive Brokers, Alpaca)
- [ ] Backtesting engine
- [ ] Advanced charting with candlesticks
- [ ] Email/SMS alerts
- [ ] Mobile app
- [ ] Machine learning predictions
- [ ] Options analysis
- [ ] Crypto trading support

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Contact: your-email@example.com

## Acknowledgments

- Stock data provided by Yahoo Finance (yfinance)
- Technical analysis powered by TA-Lib
- UI framework by Bootstrap
- Icons by Font Awesome

---

**Happy Trading! 📈**

Remember: It's not about being right all the time, it's about managing risk and letting winners run while cutting losses short.
