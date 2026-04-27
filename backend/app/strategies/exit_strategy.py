import pandas as pd
import numpy as np
from config import Config

class ExitStrategyPlanner:
    """Plans exit strategies for profit maximization"""
    
    @staticmethod
    def calculate_exit_points(entry_price, atr_value=None, use_targets=True):
        """
        Calculate exit points for 1x to 4x+ returns
        
        Args:
            entry_price: Entry price of the stock
            atr_value: Average True Range for dynamic stop loss
            use_targets: If True, use predefined targets from config
        
        Returns:
            Dictionary with stop loss and take profit targets
        """
        if entry_price <= 0:
            return None
        
        stop_loss_price = entry_price * (1 - Config.STOP_LOSS_PERCENT)
        
        # Define take profit targets
        if use_targets:
            targets = {}
            for target_multiplier in Config.TAKE_PROFIT_TARGETS:
                target_price = entry_price * (1 + (target_multiplier - 1))
                profit_percent = ((target_price - entry_price) / entry_price) * 100
                targets[f"{target_multiplier}x_return"] = {
                    'price': round(target_price, 2),
                    'return_percent': round(profit_percent, 2),
                    'quantity_to_sell': None  # To be calculated by user
                }
        
        return {
            'entry_price': entry_price,
            'stop_loss': {
                'price': round(stop_loss_price, 2),
                'loss_percent': round(-Config.STOP_LOSS_PERCENT * 100, 2)
            },
            'take_profit_targets': targets,
            'risk_reward_ratio': Config.RISK_REWARD_RATIO
        }
    
    @staticmethod
    def pyramiding_strategy(entry_price, capital, num_tranches=4):
        """
        Pyramiding strategy - Enter in multiple tranches to reduce average entry price
        
        Args:
            entry_price: Initial entry price
            capital: Total capital to invest
            num_tranches: Number of entry points
        
        Returns:
            Pyramiding plan with entry points and quantities
        """
        capital_per_tranche = capital / num_tranches
        pyramiding_plan = []
        
        # First entry at market price
        price_deviation = 0.02  # 2% deviation per tranche
        
        for i in range(num_tranches):
            adjusted_price = entry_price * (1 - (price_deviation * i))
            quantity = capital_per_tranche / adjusted_price
            
            pyramiding_plan.append({
                'tranche': i + 1,
                'entry_price': round(adjusted_price, 2),
                'quantity': round(quantity, 2),
                'capital_allocated': round(capital_per_tranche, 2)
            })
        
        # Calculate average entry price
        total_quantity = sum(p['quantity'] for p in pyramiding_plan)
        avg_entry = (capital / total_quantity) if total_quantity > 0 else entry_price
        
        return {
            'pyramiding_plan': pyramiding_plan,
            'average_entry_price': round(avg_entry, 2),
            'total_capital': capital,
            'total_quantity': round(total_quantity, 2)
        }
    
    @staticmethod
    def scaling_out_strategy(entry_price, quantity, targets=None):
        """
        Scaling out strategy - Sell portions at each target
        
        Args:
            entry_price: Entry price
            quantity: Total quantity to sell
            targets: List of target multipliers
        
        Returns:
            Scaling out plan with profit targets and quantities to sell
        """
        if targets is None:
            targets = Config.TAKE_PROFIT_TARGETS
        
        if quantity <= 0 or entry_price <= 0:
            return None
        
        scaling_plan = []
        quantity_remaining = quantity
        num_targets = len(targets)
        
        for idx, target in enumerate(targets):
            if idx == num_targets - 1:
                # Sell all remaining at last target
                qty_to_sell = quantity_remaining
            else:
                # Sell equal portions
                qty_to_sell = quantity / num_targets
            
            target_price = entry_price * target
            profit_per_unit = target_price - entry_price
            total_profit = profit_per_unit * qty_to_sell
            
            scaling_plan.append({
                'target': f"{target}x Return",
                'target_price': round(target_price, 2),
                'quantity_to_sell': round(qty_to_sell, 2),
                'profit_per_unit': round(profit_per_unit, 2),
                'total_profit': round(total_profit, 2),
                'cumulative_profit': round(profit_per_unit * qty_to_sell + (idx * quantity/num_targets * profit_per_unit), 2) if idx > 0 else round(total_profit, 2)
            })
            
            quantity_remaining -= qty_to_sell
        
        return {
            'entry_price': entry_price,
            'total_quantity': quantity,
            'scaling_plan': scaling_plan
        }
    
    @staticmethod
    def trailing_stop_strategy(current_price, entry_price, atr_value, trailing_percent=0.05):
        """
        Trailing stop strategy - Dynamic stop loss that follows price up
        
        Args:
            current_price: Current stock price
            entry_price: Entry price
            atr_value: Average True Range
            trailing_percent: Trailing stop percentage
        
        Returns:
            Trailing stop information
        """
        trailing_stop = current_price * (1 - trailing_percent)
        profit = current_price - entry_price
        profit_percent = (profit / entry_price) * 100 if entry_price > 0 else 0
        
        return {
            'current_price': round(current_price, 2),
            'entry_price': entry_price,
            'trailing_stop': round(trailing_stop, 2),
            'atr_based_stop': round(current_price - atr_value, 2) if atr_value else None,
            'current_profit': round(profit, 2),
            'profit_percent': round(profit_percent, 2),
            'trailing_stop_distance': round((current_price - trailing_stop), 2)
        }
    
    @staticmethod
    def risk_management_rules(entry_price, capital_allocated, max_risk_percent=0.02):
        """
        Risk management guidelines
        
        Args:
            entry_price: Entry price
            capital_allocated: Capital allocated to this trade
            max_risk_percent: Maximum risk as percentage of capital (default 2%)
        
        Returns:
            Risk management metrics
        """
        max_loss = capital_allocated * max_risk_percent
        stop_loss_price = entry_price * (1 - Config.STOP_LOSS_PERCENT)
        loss_per_share = entry_price - stop_loss_price
        max_shares = max_loss / loss_per_share if loss_per_share > 0 else 0
        
        return {
            'capital_allocated': round(capital_allocated, 2),
            'max_risk_percent': max_risk_percent * 100,
            'max_allowable_loss': round(max_loss, 2),
            'entry_price': round(entry_price, 2),
            'stop_loss_price': round(stop_loss_price, 2),
            'loss_per_share': round(loss_per_share, 2),
            'max_shares_to_buy': round(max_shares, 2),
            'recommended_quantity': round(max_shares * 0.8, 2)  # Conservative approach
        }
