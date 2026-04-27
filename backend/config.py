import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', False)
    
    # Stock analysis settings
    SHORT_MA_WINDOW = 20
    LONG_MA_WINDOW = 50
    RSI_PERIOD = 14
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    
    # Trading settings
    MIN_DAILY_RETURN = 0.01  # 1% minimum daily return for analysis
    RISK_REWARD_RATIO = 1.5  # 1.5x risk-reward minimum
    STOP_LOSS_PERCENT = 0.05  # 5% stop loss
    TAKE_PROFIT_TARGETS = [0.25, 0.50, 1.0, 2.0, 4.0]  # 25%, 50%, 1x, 2x, 4x
    
    # Market data settings
    DATA_PERIOD = "1y"  # 1 year of historical data
    INTERVAL = "1d"  # Daily data

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
