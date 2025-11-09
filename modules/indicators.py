"""
Indicator Library Module
Provides all technical indicators used in the scanner
"""

import pandas as pd
import numpy as np
import ta
from ta.trend import EMAIndicator, SMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator


class IndicatorLibrary:
    """Comprehensive indicator library with multi-timeframe support"""
    
    @staticmethod
    def safe_numeric(series):
        """Convert any pandas Series to numeric, replacing non-numeric with NaN."""
        return pd.to_numeric(series, errors='coerce')
    
    @staticmethod
    def normalize_ohlc(df):
        """Normalize OHLC data to ensure proper format"""
        df = df.copy()
        n = len(df)
        
        for col in ['Open', 'High', 'Low', 'Close']:
            if col not in df.columns:
                raise ValueError(f"Missing column {col}")
            
            vals = df[col]
            
            # Case 1: already numeric
            if pd.api.types.is_numeric_dtype(vals):
                df[col] = IndicatorLibrary.safe_numeric(vals)
                continue
            
            # Try to convert strings first
            if isinstance(vals.iloc[0], str):
                df[col] = IndicatorLibrary.safe_numeric(vals)
                continue
            
            first = vals.iloc[0]
            
            # Case 2: entire column stored as 1 big array
            if hasattr(first, "__len__") and not isinstance(first, str):
                try:
                    arr0f = np.asarray(first, dtype=float).ravel()
                    if arr0f.size == n:
                        df[col] = pd.Series(arr0f, index=df.index)
                        continue
                except Exception:
                    pass
            
            # Case 3: each cell is a 1-element array or scalar
            extracted = []
            for x in vals:
                try:
                    arr = np.asarray(x, dtype=float).ravel()
                    if arr.size > 0:
                        extracted.append(arr[-1])
                    else:
                        extracted.append(np.nan)
                except Exception:
                    try:
                        extracted.append(float(x))
                    except Exception:
                        extracted.append(np.nan)
            df[col] = pd.Series(extracted, index=df.index)
        
        # Coerce again to ensure all numeric
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = IndicatorLibrary.safe_numeric(df[col])
        
        return df
    
    @staticmethod
    def calculate_sma(df, period=20, column='Close'):
        """Simple Moving Average"""
        return df[column].rolling(window=period, min_periods=1).mean()
    
    @staticmethod
    def calculate_ema(df, period=20, column='Close'):
        """Exponential Moving Average"""
        return EMAIndicator(df[column], window=period).ema_indicator()
    
    @staticmethod
    def calculate_rsi(df, period=14, column='Close'):
        """Relative Strength Index"""
        return RSIIndicator(df[column], window=period).rsi()
    
    @staticmethod
    def calculate_macd(df, fast=12, slow=26, signal=9, column='Close'):
        """Moving Average Convergence Divergence"""
        macd_obj = MACD(df[column], window_fast=fast, window_slow=slow, window_sign=signal)
        return {
            'macd': macd_obj.macd(),
            'signal': macd_obj.macd_signal(),
            'histogram': macd_obj.macd_diff()
        }
    
    @staticmethod
    def calculate_bollinger_bands(df, period=20, std_dev=2, column='Close'):
        """Bollinger Bands"""
        bb = BollingerBands(df[column], window=period, window_dev=std_dev)
        return {
            'upper': bb.bollinger_hband(),
            'middle': bb.bollinger_mavg(),
            'lower': bb.bollinger_lband()
        }
    
    @staticmethod
    def calculate_atr(df, period=14):
        """Average True Range"""
        atr = AverageTrueRange(df['High'], df['Low'], df['Close'], window=period)
        return atr.average_true_range()
    
    @staticmethod
    def calculate_stochastic(df, period=14, smooth_k=3, smooth_d=3):
        """Stochastic Oscillator"""
        stoch = StochasticOscillator(
            df['High'], df['Low'], df['Close'],
            window=period, smooth_window=smooth_k
        )
        return {
            'k': stoch.stoch(),
            'd': stoch.stoch_signal()
        }
    
    @staticmethod
    def calculate_obv(df):
        """On Balance Volume"""
        if 'Volume' not in df.columns:
            return pd.Series(0, index=df.index)
        obv = OnBalanceVolumeIndicator(df['Close'], df['Volume'])
        return obv.on_balance_volume()
    
    @staticmethod
    def calculate_adx(df, period=14):
        """Average Directional Index"""
        adx = ADXIndicator(df['High'], df['Low'], df['Close'], window=period)
        return {
            'adx': adx.adx(),
            'di_plus': adx.adx_pos(),
            'di_minus': adx.adx_neg()
        }
    
    @staticmethod
    def yoda_indicator(df, fa=12, sa=26, sig=9, sma_length=50, 
                      length_squeeze=20, bb_mult=2.0, kc_mult=1.5):
        """
        Yoda Indicator - Combined MACD, SMA, and TTM Squeeze
        """
        df = IndicatorLibrary.normalize_ohlc(df)
        close = df['Close']
        high = df['High']
        low = df['Low']
        
        # MACD
        fast = EMAIndicator(close, window=fa).ema_indicator()
        slow = EMAIndicator(close, window=sa).ema_indicator()
        macd = fast - slow
        signal = macd.rolling(sig, min_periods=1).mean()
        
        df['MACD'] = macd
        df['Signal'] = signal
        df['MACD_Color'] = np.where(macd > macd.shift(1), 'green', 'red')
        df['Signal_Color'] = np.where(signal > signal.shift(1), 'green', 'red')
        
        # SMA
        sma = close.rolling(sma_length, min_periods=1).mean()
        df['SMA'] = sma
        df['CrossUp'] = (close.shift(1) < sma.shift(1)) & (close > sma)
        df['CrossDown'] = (close.shift(1) > sma.shift(1)) & (close < sma)
        
        # Buy/Sell signals
        wasGreen = (df['MACD_Color'].shift(1) == 'green') & (df['Signal_Color'].shift(1) == 'green')
        wasRed = (df['MACD_Color'].shift(1) == 'red') & (df['Signal_Color'].shift(1) == 'red')
        isGreen = (df['MACD_Color'] == 'green') & (df['Signal_Color'] == 'green')
        isRed = (df['MACD_Color'] == 'red') & (df['Signal_Color'] == 'red')
        
        df['Buy_MACD'] = (~wasGreen & isGreen).fillna(False)
        df['Sell_MACD'] = (~wasRed & isRed).fillna(False)
        
        # TTM Squeeze
        bb = BollingerBands(close, window=length_squeeze, window_dev=bb_mult)
        BB_upper = bb.bollinger_hband()
        BB_lower = bb.bollinger_lband()
        BB_basis = bb.bollinger_mavg()
        
        atr = AverageTrueRange(high, low, close, window=length_squeeze).average_true_range()
        KC_upper = BB_basis + atr * kc_mult
        KC_lower = BB_basis - atr * kc_mult
        
        inSqueeze = (BB_lower >= KC_lower) & (BB_upper <= KC_upper)
        df['TTM_Fired'] = (~inSqueeze) & (inSqueeze.shift(1).fillna(False))
        
        # Combined signals
        df['Buy_Signal'] = df['Buy_MACD'] | df['CrossUp']
        df['Sell_Signal'] = df['Sell_MACD'] | df['CrossDown']
        
        return df
    
    @staticmethod
    def calculate_vwap(df):
        """Volume Weighted Average Price"""
        if 'Volume' not in df.columns:
            return df['Close']
        return (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    
    @staticmethod
    def calculate_pivot_points(df):
        """Pivot Points"""
        pivot = (df['High'] + df['Low'] + df['Close']) / 3
        r1 = 2 * pivot - df['Low']
        s1 = 2 * pivot - df['High']
        r2 = pivot + (df['High'] - df['Low'])
        s2 = pivot - (df['High'] - df['Low'])
        
        return {
            'pivot': pivot,
            'r1': r1, 's1': s1,
            'r2': r2, 's2': s2
        }
    
    @staticmethod
    def calculate_ichimoku(df):
        """Ichimoku Cloud"""
        # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2
        period9_high = df['High'].rolling(window=9).max()
        period9_low = df['Low'].rolling(window=9).min()
        tenkan_sen = (period9_high + period9_low) / 2
        
        # Kijun-sen (Base Line): (26-period high + 26-period low)/2
        period26_high = df['High'].rolling(window=26).max()
        period26_low = df['Low'].rolling(window=26).min()
        kijun_sen = (period26_high + period26_low) / 2
        
        # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
        
        # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2
        period52_high = df['High'].rolling(window=52).max()
        period52_low = df['Low'].rolling(window=52).min()
        senkou_span_b = ((period52_high + period52_low) / 2).shift(26)
        
        return {
            'tenkan_sen': tenkan_sen,
            'kijun_sen': kijun_sen,
            'senkou_span_a': senkou_span_a,
            'senkou_span_b': senkou_span_b
        }
