"""
Scanner Engine Module
Main scanning logic with multi-timeframe support
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import traceback
from modules.indicators import IndicatorLibrary
from modules.patterns import ChartPatterns


class ScannerEngine:
    """Main scanner engine with multi-timeframe support"""
    
    def __init__(self):
        self.indicator_lib = IndicatorLibrary()
        self.pattern_detector = ChartPatterns()
        
        self.timeframe_map = {
            'Wave': '4h',
            'Tide': '1d',
            'SuperTide': '1wk'
        }
    
    def download_data(self, symbol, timeframe='1d', period='6mo'):
        """Download market data for a symbol"""
        try:
            # Map timeframe
            interval = timeframe
            
            # Adjust period based on timeframe
            if timeframe in ['1h', '2h', '4h']:
                period = '60d'
            elif timeframe == '15m':
                period = '7d'
            elif timeframe == '1wk':
                period = '2y'
            
            df = yf.download(symbol, period=period, interval=interval, progress=False)
            
            if df.empty:
                return None
            
            # Ensure we have OHLC columns
            if 'Close' not in df.columns:
                return None
            
            # Clean up column names if multi-level
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            return df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
        except Exception as e:
            return None
    
    def calculate_indicators(self, df, indicator_list):
        """Calculate all indicators for a dataframe"""
        try:
            df = self.indicator_lib.normalize_ohlc(df)
            
            for indicator in indicator_list:
                if indicator == 'Yoda':
                    df = self.indicator_lib.yoda_indicator(df)
                elif indicator == 'RSI':
                    df['RSI'] = self.indicator_lib.calculate_rsi(df)
                elif indicator == 'MACD':
                    macd = self.indicator_lib.calculate_macd(df)
                    df['MACD'] = macd['macd']
                    df['MACD_Signal'] = macd['signal']
                    df['MACD_Hist'] = macd['histogram']
                elif indicator == 'BB':
                    bb = self.indicator_lib.calculate_bollinger_bands(df)
                    df['BB_Upper'] = bb['upper']
                    df['BB_Middle'] = bb['middle']
                    df['BB_Lower'] = bb['lower']
                elif indicator == 'ATR':
                    df['ATR'] = self.indicator_lib.calculate_atr(df)
                elif indicator == 'ADX':
                    adx = self.indicator_lib.calculate_adx(df)
                    df['ADX'] = adx['adx']
                    df['DI_Plus'] = adx['di_plus']
                    df['DI_Minus'] = adx['di_minus']
                elif indicator == 'Stochastic':
                    stoch = self.indicator_lib.calculate_stochastic(df)
                    df['Stoch_K'] = stoch['k']
                    df['Stoch_D'] = stoch['d']
                elif indicator == 'OBV':
                    df['OBV'] = self.indicator_lib.calculate_obv(df)
                elif indicator == 'VWAP':
                    df['VWAP'] = self.indicator_lib.calculate_vwap(df)
                elif indicator == 'EMA_5':
                    df['EMA_5'] = self.indicator_lib.calculate_ema(df, 5)
                elif indicator == 'EMA_20':
                    df['EMA_20'] = self.indicator_lib.calculate_ema(df, 20)
                elif indicator == 'EMA_50':
                    df['EMA_50'] = self.indicator_lib.calculate_ema(df, 50)
                elif indicator == 'SMA_200':
                    df['SMA_200'] = self.indicator_lib.calculate_sma(df, 200)
            
            return df
        except Exception as e:
            traceback.print_exc()
            return df
    
    def calculate_patterns(self, df, pattern_list):
        """Calculate all patterns for a dataframe"""
        try:
            for pattern in pattern_list:
                if pattern == 'Double_Bottom':
                    df['Double_Bottom'] = self.pattern_detector.detect_double_bottom(df['Close'])
                elif pattern == 'Double_Top':
                    df['Double_Top'] = self.pattern_detector.detect_double_top(df['Close'])
                elif pattern == 'Head_Shoulders':
                    df['Head_Shoulders'] = self.pattern_detector.detect_head_and_shoulders(df)
                elif pattern == 'Inv_Head_Shoulders':
                    df['Inv_Head_Shoulders'] = self.pattern_detector.detect_inverse_head_and_shoulders(df)
                elif pattern == 'TL_Break_Up':
                    df['TL_Break_Up'] = self.pattern_detector.detect_trendline_breakout(df, 'up')
                elif pattern == 'TL_Break_Down':
                    df['TL_Break_Down'] = self.pattern_detector.detect_trendline_breakout(df, 'down')
                elif pattern == 'Triangle':
                    df['Triangle'] = self.pattern_detector.detect_triangle_pattern(df)
                elif pattern == 'Cup_Handle':
                    df['Cup_Handle'] = self.pattern_detector.detect_cup_and_handle(df)
                elif pattern == 'Flag':
                    df['Flag'] = self.pattern_detector.detect_flag_pattern(df)
                elif pattern == 'Rising_Wedge':
                    df['Rising_Wedge'] = self.pattern_detector.detect_wedge_pattern(df, 'rising')
                elif pattern == 'Falling_Wedge':
                    df['Falling_Wedge'] = self.pattern_detector.detect_wedge_pattern(df, 'falling')
            
            return df
        except Exception as e:
            traceback.print_exc()
            return df
    
    def scan_symbol(self, symbol, workflow):
        """Scan a single symbol with the given workflow"""
        try:
            # Get timeframes from workflow
            timeframes = workflow.get('timeframes', self.timeframe_map)
            indicators = workflow.get('indicators', ['Yoda'])
            patterns = workflow.get('patterns', [])
            setups = workflow.get('setups', [])
            
            # Download data for all timeframes
            df_dict = {}
            for tf_name, tf_interval in timeframes.items():
                df = self.download_data(symbol, tf_interval)
                if df is not None and len(df) > 0:
                    # Calculate indicators
                    df = self.calculate_indicators(df, indicators)
                    # Calculate patterns
                    df = self.calculate_patterns(df, patterns)
                    df_dict[tf_name] = df
                else:
                    df_dict[tf_name] = None
            
            # Check if we have any valid data
            if not any(df is not None for df in df_dict.values()):
                return None
            
            # Get the latest data from Tide (1d) timeframe
            tide_df = df_dict.get('Tide')
            if tide_df is None or len(tide_df) == 0:
                # Try Wave if Tide is not available
                tide_df = df_dict.get('Wave')
                if tide_df is None or len(tide_df) == 0:
                    return None
            
            last_row = tide_df.iloc[-1]
            
            # Check for signals
            has_buy_signal = bool(last_row.get('Buy_Signal', False)) if 'Buy_Signal' in tide_df.columns else False
            has_sell_signal = bool(last_row.get('Sell_Signal', False)) if 'Sell_Signal' in tide_df.columns else False
            
            # Check patterns
            detected_patterns = []
            for pattern in patterns:
                if pattern in tide_df.columns and bool(last_row.get(pattern, False)):
                    detected_patterns.append(pattern)
            
            # Evaluate setups (simplified)
            setup_results = []
            for setup_name in setups:
                if setup_name == 'Momentum_Long' and has_buy_signal:
                    setup_results.append('Momentum_Long')
                elif setup_name == 'Momentum_Short' and has_sell_signal:
                    setup_results.append('Momentum_Short')
            
            # Calculate metrics
            rsi = last_row.get('RSI', np.nan)
            macd = last_row.get('MACD', np.nan)
            
            # Multi-timeframe alignment
            mtf_signal = self._calculate_mtf_alignment(df_dict)
            
            result = {
                'Symbol': symbol,
                'Close': float(last_row['Close']),
                'Signal': 'BUY' if has_buy_signal else ('SELL' if has_sell_signal else 'NEUTRAL'),
                'RSI': float(rsi) if not pd.isna(rsi) else None,
                'MACD': float(macd) if not pd.isna(macd) else None,
                'Patterns': ', '.join(detected_patterns) if detected_patterns else '-',
                'Setups': ', '.join(setup_results) if setup_results else '-',
                'MTF_Alignment': mtf_signal,
                'Wave': '✓' if df_dict.get('Wave') is not None else '✗',
                'Tide': '✓' if df_dict.get('Tide') is not None else '✗',
                'SuperTide': '✓' if df_dict.get('SuperTide') is not None else '✗'
            }
            
            return result
            
        except Exception as e:
            traceback.print_exc()
            return {
                'Symbol': symbol,
                'Error': str(e)
            }
    
    def _calculate_mtf_alignment(self, df_dict):
        """Calculate multi-timeframe alignment score"""
        try:
            scores = []
            
            for tf_name, df in df_dict.items():
                if df is None or len(df) == 0:
                    continue
                
                last = df.iloc[-1]
                
                # Check if price is above SMA
                if 'SMA' in df.columns and 'Close' in df.columns:
                    if last['Close'] > last['SMA']:
                        scores.append(1)
                    else:
                        scores.append(-1)
                elif 'Buy_Signal' in df.columns:
                    if last.get('Buy_Signal', False):
                        scores.append(1)
                    elif last.get('Sell_Signal', False):
                        scores.append(-1)
            
            if not scores:
                return 'Neutral'
            
            avg_score = np.mean(scores)
            if avg_score > 0.5:
                return 'Bullish ⬆'
            elif avg_score < -0.5:
                return 'Bearish ⬇'
            else:
                return 'Neutral ⬌'
                
        except Exception:
            return 'N/A'
    
    def scan_multiple_symbols(self, symbols, workflow, progress_callback=None):
        """Scan multiple symbols"""
        results = []
        total = len(symbols)
        
        for i, symbol in enumerate(symbols):
            if progress_callback:
                progress_callback(i + 1, total, symbol)
            
            result = self.scan_symbol(symbol, workflow)
            if result:
                results.append(result)
        
        return pd.DataFrame(results)
