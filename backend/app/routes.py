from flask import Blueprint, request, jsonify
from app.models.stock_data import StockDataManager
from app.strategies.analysis import TechnicalAnalyzer
from app.strategies.signals import SignalGenerator
from app.strategies.exit_strategy import ExitStrategyPlanner
import traceback

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize data manager
data_manager = StockDataManager()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

@api_bp.route('/stock/analyze', methods=['POST'])
def analyze_stock():
    """
    Analyze stock with technical indicators and generate signals
    
    POST Body:
    {
        "symbol": "AAPL",
        "period": "1y",
        "interval": "1d"
    }
    """
    try:
        data = request.json
        symbol = data.get('symbol', '').upper()
        period = data.get('period', '1y')
        interval = data.get('interval', '1d')
        
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
        
        # Fetch stock data
        stock_data = data_manager.get_stock_data(symbol, period, interval)
        if stock_data is None or stock_data.empty:
            return jsonify({'error': f'Could not fetch data for {symbol}'}), 404
        
        # Perform technical analysis
        analyzed_data = TechnicalAnalyzer.full_analysis(stock_data.copy())
        
        # Get latest values for response
        latest = analyzed_data.iloc[-1]
        
        # Generate signals
        signal, signal_info = SignalGenerator.get_combined_signal(analyzed_data)
        momentum = SignalGenerator.get_momentum_strength(analyzed_data)
        price_momentum = SignalGenerator.get_price_momentum(analyzed_data)
        
        # Get stock info
        stock_info = data_manager.get_stock_info(symbol)
        
        return jsonify({
            'symbol': symbol,
            'current_price': float(latest['Close']),
            'previous_close': float(analyzed_data.iloc[-2]['Close']) if len(analyzed_data) > 1 else 0,
            'daily_change': float(latest['Daily_Return']) if not pd.isna(latest['Daily_Return']) else 0,
            'technical_indicators': {
                'sma_20': float(latest['SMA_Short']) if not pd.isna(latest['SMA_Short']) else None,
                'sma_50': float(latest['SMA_Long']) if not pd.isna(latest['SMA_Long']) else None,
                'rsi': float(latest['RSI']) if not pd.isna(latest['RSI']) else None,
                'macd': float(latest['MACD']) if not pd.isna(latest['MACD']) else None,
                'macd_signal': float(latest['MACD_Signal']) if not pd.isna(latest['MACD_Signal']) else None,
                'bollinger_upper': float(latest['BB_Upper']) if not pd.isna(latest['BB_Upper']) else None,
                'bollinger_middle': float(latest['BB_Middle']) if not pd.isna(latest['BB_Middle']) else None,
                'bollinger_lower': float(latest['BB_Lower']) if not pd.isna(latest['BB_Lower']) else None,
                'atr': float(latest['ATR']) if not pd.isna(latest['ATR']) else None
            },
            'signal': signal,
            'signal_details': signal_info,
            'momentum': {
                'rsi_momentum': momentum,
                'price_momentum_5d': price_momentum
            },
            'stock_info': stock_info,
            'timestamp': str(analyzed_data.index[-1])
        }), 200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stock/exit-plan', methods=['POST'])
def get_exit_plan():
    """
    Get exit strategy plan for a stock
    
    POST Body:
    {
        "entry_price": 150.00,
        "current_price": 155.00,
        "quantity": 100,
        "capital_allocated": 15000
    }
    """
    try:
        data = request.json
        entry_price = float(data.get('entry_price', 0))
        current_price = float(data.get('current_price', entry_price))
        quantity = float(data.get('quantity', 0))
        capital_allocated = float(data.get('capital_allocated', 0))
        
        if entry_price <= 0:
            return jsonify({'error': 'Valid entry price is required'}), 400
        
        # Calculate exit points
        exit_points = ExitStrategyPlanner.calculate_exit_points(entry_price)
        
        # Pyramiding strategy
        if capital_allocated > 0:
            pyramiding = ExitStrategyPlanner.pyramiding_strategy(entry_price, capital_allocated)
        else:
            pyramiding = None
        
        # Scaling out strategy
        if quantity > 0:
            scaling_out = ExitStrategyPlanner.scaling_out_strategy(entry_price, quantity)
        else:
            scaling_out = None
        
        # Risk management rules
        if capital_allocated > 0:
            risk_mgmt = ExitStrategyPlanner.risk_management_rules(entry_price, capital_allocated)
        else:
            risk_mgmt = None
        
        return jsonify({
            'exit_points': exit_points,
            'pyramiding_strategy': pyramiding,
            'scaling_out_strategy': scaling_out,
            'risk_management': risk_mgmt,
            'current_stats': {
                'current_price': current_price,
                'entry_price': entry_price,
                'profit_loss': round(current_price - entry_price, 2),
                'profit_loss_percent': round(((current_price - entry_price) / entry_price) * 100, 2),
                'quantity_owned': quantity
            }
        }), 200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stock/compare', methods=['POST'])
def compare_stocks():
    """
    Compare multiple stocks
    
    POST Body:
    {
        "symbols": ["AAPL", "GOOGL", "MSFT"]
    }
    """
    try:
        data = request.json
        symbols = data.get('symbols', [])
        
        if not symbols:
            return jsonify({'error': 'At least one symbol is required'}), 400
        
        comparison_results = []
        
        for symbol in symbols:
            symbol = symbol.upper()
            stock_data = data_manager.get_stock_data(symbol)
            
            if stock_data is not None and not stock_data.empty:
                analyzed_data = TechnicalAnalyzer.full_analysis(stock_data.copy())
                signal, _ = SignalGenerator.get_combined_signal(analyzed_data)
                momentum = SignalGenerator.get_momentum_strength(analyzed_data)
                latest = analyzed_data.iloc[-1]
                
                comparison_results.append({
                    'symbol': symbol,
                    'price': float(latest['Close']),
                    'daily_return': float(latest['Daily_Return']) if not pd.isna(latest['Daily_Return']) else 0,
                    'signal': signal,
                    'rsi': float(latest['RSI']) if not pd.isna(latest['RSI']) else None,
                    'momentum': momentum
                })
        
        # Sort by signal strength and momentum
        signal_order = {'STRONG_BUY': 5, 'BUY': 4, 'WEAK_BUY': 3, 'NEUTRAL': 2, 'WEAK_SELL': 1, 'SELL': 0, 'STRONG_SELL': -1}
        comparison_results.sort(key=lambda x: (signal_order.get(x['signal'], 0), x['momentum']), reverse=True)
        
        return jsonify({
            'comparison': comparison_results,
            'total_analyzed': len(comparison_results)
        }), 200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stock/screener', methods=['GET'])
def stock_screener():
    """
    Screen for high potential stocks (1x to 4x+ returns)
    Filters stocks by momentum and signal strength
    """
    try:
        # Default list of promising stocks
        watchlist = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA', 'META', 'AMD', 'CRM', 'SHOP']
        
        screener_results = []
        
        for symbol in watchlist:
            try:
                stock_data = data_manager.get_stock_data(symbol)
                
                if stock_data is not None and not stock_data.empty:
                    analyzed_data = TechnicalAnalyzer.full_analysis(stock_data.copy())
                    signal, signal_info = SignalGenerator.get_combined_signal(analyzed_data)
                    momentum = SignalGenerator.get_momentum_strength(analyzed_data)
                    price_momentum = SignalGenerator.get_price_momentum(analyzed_data, 10)
                    latest = analyzed_data.iloc[-1]
                    
                    # Calculate score
                    score = signal_info['individual_scores'].get('SMA', 0) + \
                            signal_info['individual_scores'].get('RSI', 0) + \
                            signal_info['individual_scores'].get('MACD', 0) + \
                            signal_info['individual_scores'].get('Bollinger', 0)
                    
                    screener_results.append({
                        'symbol': symbol,
                        'price': round(float(latest['Close']), 2),
                        'signal': signal,
                        'score': score,
                        'momentum': round(momentum, 2),
                        'price_momentum_10d': round(price_momentum, 2),
                        'rsi': round(float(latest['RSI']), 2) if not pd.isna(latest['RSI']) else None,
                        'recommendation': 'WATCH' if score >= 2 else 'CONSIDER'
                    })
            except:
                continue
        
        # Sort by score and momentum
        screener_results.sort(key=lambda x: (x['score'], x['momentum']), reverse=True)
        
        return jsonify({
            'screener_results': screener_results,
            'total_screened': len(screener_results),
            'high_potential': [s for s in screener_results if s['score'] >= 2]
        }), 200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stock/trending', methods=['GET'])
def get_trending_stocks():
    """Get stocks with strongest signals"""
    try:
        watchlist = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', 'AMD']
        trending = []
        
        for symbol in watchlist:
            try:
                stock_data = data_manager.get_stock_data(symbol)
                if stock_data is not None and not stock_data.empty:
                    analyzed_data = TechnicalAnalyzer.full_analysis(stock_data.copy())
                    signal, _ = SignalGenerator.get_combined_signal(analyzed_data)
                    latest = analyzed_data.iloc[-1]
                    
                    trending.append({
                        'symbol': symbol,
                        'price': round(float(latest['Close']), 2),
                        'signal': signal,
                        'daily_change': round(float(latest['Daily_Return']), 2) if not pd.isna(latest['Daily_Return']) else 0
                    })
            except:
                continue
        
        return jsonify({'trending': trending}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Import pandas for data handling
import pandas as pd
