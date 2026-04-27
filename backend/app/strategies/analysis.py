import pandas as pd
import numpy as np
import ta
from config import Config

class TechnicalAnalyzer:
    """Performs technical analysis on stock data"""
    
    @staticmethod
    def calculate_moving_averages(data, short_window=Config.SHORT_MA_WINDOW, long_window=Config.LONG_MA_WINDOW):
        """Calculate short and long term moving averages"""
        data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
        data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
        return data
    
    @staticmethod
    def calculate_rsi(data, period=Config.RSI_PERIOD):
        """Calculate Relative Strength Index"""
        try:
            # Try with 'length' parameter first
            data['RSI'] = ta.momentum.rsi(data['Close'], length=period)
        except TypeError:
            # If that fails, calculate RSI manually
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
        return data
    
    @staticmethod
    def calculate_macd(data, fast=Config.MACD_FAST, slow=Config.MACD_SLOW, signal=Config.MACD_SIGNAL):
        """Calculate MACD (Moving Average Convergence Divergence)"""
        try:
            data['MACD'] = ta.trend.macd(data['Close'], window_fast=fast, window_slow=slow)
            data['MACD_Signal'] = ta.trend.macd_signal(data['Close'], window_fast=fast, window_slow=slow, window_sign=signal)
            data['MACD_Diff'] = ta.trend.macd_diff(data['Close'], window_fast=fast, window_slow=slow, window_sign=signal)
        except (TypeError, AttributeError):
            # Calculate MACD manually
            ema_fast = data['Close'].ewm(span=fast, adjust=False).mean()
            ema_slow = data['Close'].ewm(span=slow, adjust=False).mean()
            data['MACD'] = ema_fast - ema_slow
            data['MACD_Signal'] = data['MACD'].ewm(span=signal, adjust=False).mean()
            data['MACD_Diff'] = data['MACD'] - data['MACD_Signal']
        return data
    
    @staticmethod
    def calculate_bollinger_bands(data, period=20, num_std=2):
        """Calculate Bollinger Bands"""
        data['BB_Middle'] = data['Close'].rolling(window=period).mean()
        std = data['Close'].rolling(window=period).std()
        data['BB_Upper'] = data['BB_Middle'] + (std * num_std)
        data['BB_Lower'] = data['BB_Middle'] - (std * num_std)
        data['BB_Width'] = data['BB_Upper'] - data['BB_Lower']
        return data
    
    @staticmethod
    def calculate_atr(data, period=14):
        """Calculate Average True Range"""
        try:
            data['ATR'] = ta.volatility.average_true_range(data['High'], data['Low'], data['Close'], length=period)
        except (TypeError, AttributeError):
            # Calculate ATR manually
            data['TR'] = np.maximum(
                data['High'] - data['Low'],
                np.maximum(
                    np.abs(data['High'] - data['Close'].shift()),
                    np.abs(data['Low'] - data['Close'].shift())
                )
            )
            data['ATR'] = data['TR'].rolling(window=period).mean()
        return data
    
    @staticmethod
    def calculate_daily_returns(data):
        """Calculate daily percentage returns"""
        data['Daily_Return'] = data['Close'].pct_change() * 100
        return data
    
    @staticmethod
    def full_analysis(data):
        """Perform complete technical analysis"""
        data = TechnicalAnalyzer.calculate_moving_averages(data)
        data = TechnicalAnalyzer.calculate_rsi(data)
        data = TechnicalAnalyzer.calculate_macd(data)
        data = TechnicalAnalyzer.calculate_bollinger_bands(data)
        data = TechnicalAnalyzer.calculate_atr(data)
        data = TechnicalAnalyzer.calculate_daily_returns(data)
        return data
