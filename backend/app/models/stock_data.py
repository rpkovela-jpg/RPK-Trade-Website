import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from config import Config

class StockDataManager:
    """Manages stock data retrieval and caching"""
    
    def __init__(self):
        self.cache = {}
    
    def get_stock_data(self, symbol, period=Config.DATA_PERIOD, interval=Config.INTERVAL):
        """
        Fetch stock data from Yahoo Finance
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval: Data interval ('1m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        
        Returns:
            DataFrame with stock OHLCV data or None if error
        """
        try:
            cache_key = f"{symbol}_{period}_{interval}"
            
            # Return cached data if available and fresh (within 1 hour)
            if cache_key in self.cache:
                data, timestamp = self.cache[cache_key]
                if datetime.now() - timestamp < timedelta(hours=1):
                    return data
            
            # Fetch fresh data
            stock = yf.Ticker(symbol)
            data = stock.history(period=period, interval=interval)
            
            if data.empty:
                return None
            
            # Cache the data
            self.cache[cache_key] = (data, datetime.now())
            
            return data
        
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {str(e)}")
            return None
    
    def get_current_price(self, symbol):
        """Get current price of stock"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period='1d')
            if data.empty:
                return None
            return float(data['Close'].iloc[-1])
        except Exception as e:
            print(f"Error fetching current price for {symbol}: {str(e)}")
            return None
    
    def get_stock_info(self, symbol):
        """Get stock information"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            return {
                'symbol': symbol,
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                '52_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                '52_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
            }
        except Exception as e:
            print(f"Error fetching stock info for {symbol}: {str(e)}")
            return None
