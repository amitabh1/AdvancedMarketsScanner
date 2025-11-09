"""
Rule Engine Module
Handles complex rule evaluation with AND/OR logic
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any


class RuleEngine:
    """
    Rule engine for evaluating complex conditions with AND/OR logic
    Example: IF (RSI > 60 OR MACD > 0) AND ADX > 18 AND Price > 5_EMA
    """
    
    def __init__(self):
        self.operators = {
            '>': lambda a, b: a > b,
            '<': lambda a, b: a < b,
            '>=': lambda a, b: a >= b,
            '<=': lambda a, b: a <= b,
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
        }
    
    def evaluate_condition(self, df: pd.DataFrame, condition: Dict) -> bool:
        """
        Evaluate a single condition
        condition format: {'indicator': 'RSI', 'operator': '>', 'value': 60}
        or: {'indicator': 'Close', 'operator': '>', 'reference': 'EMA_5'}
        """
        try:
            indicator = condition.get('indicator')
            operator = condition.get('operator')
            
            if indicator not in df.columns:
                return False
            
            left_value = df[indicator].iloc[-1]
            
            # Check if comparing to another indicator or a fixed value
            if 'reference' in condition:
                reference = condition['reference']
                if reference not in df.columns:
                    return False
                right_value = df[reference].iloc[-1]
            else:
                right_value = condition.get('value', 0)
            
            # Handle NaN values
            if pd.isna(left_value) or pd.isna(right_value):
                return False
            
            # Evaluate the condition
            op_func = self.operators.get(operator)
            if op_func:
                return bool(op_func(left_value, right_value))
            
            return False
        except Exception as e:
            return False
    
    def evaluate_rule(self, df: pd.DataFrame, rule: Dict) -> bool:
        """
        Evaluate a rule with AND/OR logic
        
        Rule format:
        {
            'type': 'AND',  # or 'OR'
            'conditions': [
                {'indicator': 'RSI', 'operator': '>', 'value': 60},
                {
                    'type': 'OR',
                    'conditions': [
                        {'indicator': 'MACD', 'operator': '>', 'value': 0},
                        {'indicator': 'ADX', 'operator': '>', 'value': 18}
                    ]
                }
            ]
        }
        """
        try:
            rule_type = rule.get('type', 'AND')
            conditions = rule.get('conditions', [])
            
            if not conditions:
                return False
            
            results = []
            for condition in conditions:
                if 'type' in condition:
                    # Nested rule
                    result = self.evaluate_rule(df, condition)
                else:
                    # Single condition
                    result = self.evaluate_condition(df, condition)
                results.append(result)
            
            if rule_type == 'AND':
                return all(results)
            elif rule_type == 'OR':
                return any(results)
            else:
                return False
                
        except Exception as e:
            return False
    
    def parse_text_rule(self, text: str) -> Dict:
        """
        Parse a text rule into a structured format
        Example: "RSI > 60 OR MACD > 0" -> structured rule dict
        """
        try:
            text = text.strip()
            
            # Check for AND/OR at the top level
            if ' AND ' in text:
                parts = text.split(' AND ')
                return {
                    'type': 'AND',
                    'conditions': [self.parse_text_rule(part.strip()) for part in parts]
                }
            elif ' OR ' in text:
                parts = text.split(' OR ')
                return {
                    'type': 'OR',
                    'conditions': [self.parse_text_rule(part.strip()) for part in parts]
                }
            else:
                # Single condition
                for op in ['>=', '<=', '>', '<', '==', '!=']:
                    if op in text:
                        parts = text.split(op)
                        if len(parts) == 2:
                            indicator = parts[0].strip()
                            value_str = parts[1].strip()
                            
                            # Check if value is a number or another indicator
                            try:
                                value = float(value_str)
                                return {
                                    'indicator': indicator,
                                    'operator': op,
                                    'value': value
                                }
                            except ValueError:
                                return {
                                    'indicator': indicator,
                                    'operator': op,
                                    'reference': value_str
                                }
            
            return {}
        except Exception as e:
            return {}


class SetupLibrary:
    """Predefined trading setups"""
    
    @staticmethod
    def get_momentum_long():
        """Momentum Long Setup"""
        return {
            'name': 'Momentum Long',
            'description': 'Multi-timeframe momentum alignment for long entries',
            'timeframes': {
                'Wave': {
                    'rules': [
                        {
                            'type': 'AND',
                            'conditions': [
                                {'indicator': 'RSI', 'operator': '>', 'value': 50},
                                {'indicator': 'MACD', 'operator': '>', 'value': 0}
                            ]
                        }
                    ]
                },
                'Tide': {
                    'rules': [
                        {
                            'type': 'AND',
                            'conditions': [
                                {'indicator': 'Buy_Signal', 'operator': '==', 'value': True},
                                {'indicator': 'Close', 'operator': '>', 'reference': 'SMA'}
                            ]
                        }
                    ]
                },
                'SuperTide': {
                    'rules': [
                        {
                            'type': 'OR',
                            'conditions': [
                                {'indicator': 'Close', 'operator': '>', 'reference': 'SMA'},
                                {'indicator': 'TTM_Fired', 'operator': '==', 'value': True}
                            ]
                        }
                    ]
                }
            },
            'logic': 'Wave AND Tide AND SuperTide'
        }
    
    @staticmethod
    def get_momentum_short():
        """Momentum Short Setup"""
        return {
            'name': 'Momentum Short',
            'description': 'Multi-timeframe momentum alignment for short entries',
            'timeframes': {
                'Wave': {
                    'rules': [
                        {
                            'type': 'AND',
                            'conditions': [
                                {'indicator': 'RSI', 'operator': '<', 'value': 50},
                                {'indicator': 'MACD', 'operator': '<', 'value': 0}
                            ]
                        }
                    ]
                },
                'Tide': {
                    'rules': [
                        {
                            'type': 'AND',
                            'conditions': [
                                {'indicator': 'Sell_Signal', 'operator': '==', 'value': True},
                                {'indicator': 'Close', 'operator': '<', 'reference': 'SMA'}
                            ]
                        }
                    ]
                },
                'SuperTide': {
                    'rules': [
                        {
                            'type': 'OR',
                            'conditions': [
                                {'indicator': 'Close', 'operator': '<', 'reference': 'SMA'},
                                {'indicator': 'TTM_Fired', 'operator': '==', 'value': True}
                            ]
                        }
                    ]
                }
            },
            'logic': 'Wave AND Tide'
        }
    
    @staticmethod
    def get_breakout_setup():
        """Breakout Setup"""
        return {
            'name': 'Breakout',
            'description': 'Price breakout with volume confirmation',
            'timeframes': {
                'Wave': {
                    'rules': [
                        {
                            'type': 'OR',
                            'conditions': [
                                {'indicator': 'TL_Break_Up', 'operator': '==', 'value': True},
                                {'indicator': 'Double_Bottom', 'operator': '==', 'value': True}
                            ]
                        }
                    ]
                },
                'Tide': {
                    'rules': [
                        {
                            'type': 'AND',
                            'conditions': [
                                {'indicator': 'RSI', 'operator': '>', 'value': 40},
                                {'indicator': 'RSI', 'operator': '<', 'value': 70}
                            ]
                        }
                    ]
                }
            },
            'logic': 'Wave AND Tide'
        }
    
    @staticmethod
    def get_all_setups():
        """Get all predefined setups"""
        return {
            'Momentum_Long': SetupLibrary.get_momentum_long(),
            'Momentum_Short': SetupLibrary.get_momentum_short(),
            'Breakout': SetupLibrary.get_breakout_setup()
        }
