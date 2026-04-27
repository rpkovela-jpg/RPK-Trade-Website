import pandas as pd
import numpy as np
from config import Config

class SignalGenerator:
    """Generates buy/sell signals based on technical analysis"""
    
    @staticmethod
    def get_sma_signal(data):
        """
        SMA Crossover Signal
        Buy: Short MA > Long MA
        Sell: Short MA < Long MA
        """
        if pd.isna(data['SMA_Short'].iloc[-1]) or pd.isna(data['SMA_Long'].iloc[-1]):
            return 'NEUTRAL', 0
        
        if data['SMA_Short'].iloc[-1] > data['SMA_Long'].iloc[-1]:
            return 'BUY', 1
        elif data['SMA_Short'].iloc[-1] < data['SMA_Long'].iloc[-1]:
            return 'SELL', -1
        return 'NEUTRAL', 0
    
    @staticmethod
    def get_rsi_signal(data):
        """
        RSI Signal
        Buy: RSI < 30 (Oversold)
        Sell: RSI > 70 (Overbought)
        Neutral: 30-70
        """
        rsi = data['RSI'].iloc[-1]
        if pd.isna(rsi):
            return 'NEUTRAL', 0
        
        if rsi < 30:
            return 'BUY', 1
        elif rsi > 70:
            return 'SELL', -1
        return 'NEUTRAL', 0
    
    @staticmethod
    def get_macd_signal(data):
        """
        MACD Signal
        Buy: MACD > Signal Line
        Sell: MACD < Signal Line
        """
        macd = data['MACD'].iloc[-1]
        signal = data['MACD_Signal'].iloc[-1]
        
        if pd.isna(macd) or pd.isna(signal):
            return 'NEUTRAL', 0
        
        if macd > signal:
            return 'BUY', 1
        elif macd < signal:
            return 'SELL', -1
        return 'NEUTRAL', 0
    
    @staticmethod
    def get_bollinger_signal(data):
        """
        Bollinger Bands Signal
        Buy: Price < Lower Band (Oversold)
        Sell: Price > Upper Band (Overbought)
        """
        close = data['Close'].iloc[-1]
        upper = data['BB_Upper'].iloc[-1]
        lower = data['BB_Lower'].iloc[-1]
        
        if pd.isna(upper) or pd.isna(lower):
            return 'NEUTRAL', 0
        
        if close < lower:
            return 'BUY', 1
        elif close > upper:
            return 'SELL', -1
        return 'NEUTRAL', 0
    
    @staticmethod
    def get_combined_signal(data):
        """
        Combined Signal from all indicators
        Returns the most agreed-upon signal
        """
        sma_signal, sma_score = SignalGenerator.get_sma_signal(data)
        rsi_signal, rsi_score = SignalGenerator.get_rsi_signal(data)
        macd_signal, macd_score = SignalGenerator.get_macd_signal(data)
        bb_signal, bb_score = SignalGenerator.get_bollinger_signal(data)
        
        # Calculate weighted score
        total_score = sma_score + rsi_score + macd_score + bb_score
        
        signals_info = {
            'SMA': sma_signal,
            'RSI': rsi_signal,
            'MACD': macd_signal,
            'Bollinger': bb_signal,
            'individual_scores': {
                'SMA': sma_score,
                'RSI': rsi_score,
                'MACD': macd_score,
                'Bollinger': bb_score
            }
        }
        
        # Determine overall signal
        if total_score >= 3:
            return 'STRONG_BUY', signals_info
        elif total_score == 2:
            return 'BUY', signals_info
        elif total_score == 1:
            return 'WEAK_BUY', signals_info
        elif total_score == -1:
            return 'WEAK_SELL', signals_info
        elif total_score == -2:
            return 'SELL', signals_info
        elif total_score <= -3:
            return 'STRONG_SELL', signals_info
        else:
            return 'NEUTRAL', signals_info
    
    @staticmethod
    def get_momentum_strength(data):
        """Calculate momentum strength (0-100)"""
        rsi = data['RSI'].iloc[-1]
        if pd.isna(rsi):
            return 50
        
        # RSI is already 0-100
        return float(rsi)
    
    @staticmethod
    def get_price_momentum(data, periods=5):
        """Get price momentum over last N periods"""
        if len(data) < periods:
            return 0
        
        current = data['Close'].iloc[-1]
        previous = data['Close'].iloc[-periods]
        momentum = ((current - previous) / previous) * 100
        return float(momentum)
