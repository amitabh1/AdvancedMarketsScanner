"""
Chart Patterns Module
Detects various chart patterns in price data
"""

import pandas as pd
import numpy as np
from scipy.signal import argrelextrema


class ChartPatterns:
    """Detects chart patterns in OHLC data"""
    
    @staticmethod
    def safe_last_bool(x):
        """Safely extract last boolean value"""
        try:
            if isinstance(x, pd.Series):
                if x.empty:
                    return False
                return bool(x.iloc[-1])
            if isinstance(x, (np.ndarray, list)):
                arr = np.asarray(x).ravel()
                return bool(arr[-1]) if arr.size else False
            return bool(x)
        except Exception:
            return False
    
    @staticmethod
    def detect_double_bottom(close, lookback=50, tolerance=0.02):
        """
        Detect double bottom pattern
        Returns a Series of boolean values
        """
        s = np.asarray(close).astype(float).ravel()
        n = len(s)
        res = np.zeros(n, dtype=bool)
        
        if n < 5:
            return pd.Series(res, index=close.index)
        
        # Find local minima
        minima = (np.roll(s, 1) > s) & (np.roll(s, -1) > s)
        minima[0] = minima[-1] = False
        
        for i in range(n):
            start = max(0, i - lookback)
            local = minima[start:i + 1]
            idxs = np.where(local)[0]
            
            if len(idxs) >= 2:
                v1 = s[start + idxs[-2]]
                v2 = s[start + idxs[-1]]
                if abs(v1 - v2) / ((v1 + v2) / 2 + 1e-9) <= tolerance:
                    res[i] = True
        
        return pd.Series(res, index=close.index)
    
    @staticmethod
    def detect_double_top(close, lookback=50, tolerance=0.02):
        """
        Detect double top pattern
        Returns a Series of boolean values
        """
        s = np.asarray(close).astype(float).ravel()
        n = len(s)
        res = np.zeros(n, dtype=bool)
        
        if n < 5:
            return pd.Series(res, index=close.index)
        
        # Find local maxima
        maxima = (np.roll(s, 1) < s) & (np.roll(s, -1) < s)
        maxima[0] = maxima[-1] = False
        
        for i in range(n):
            start = max(0, i - lookback)
            local = maxima[start:i + 1]
            idxs = np.where(local)[0]
            
            if len(idxs) >= 2:
                v1 = s[start + idxs[-2]]
                v2 = s[start + idxs[-1]]
                if abs(v1 - v2) / ((v1 + v2) / 2 + 1e-9) <= tolerance:
                    res[i] = True
        
        return pd.Series(res, index=close.index)
    
    @staticmethod
    def detect_head_and_shoulders(df, lookback=50):
        """
        Detect head and shoulders pattern
        """
        close = np.asarray(df['Close']).astype(float).ravel()
        n = len(close)
        res = np.zeros(n, dtype=bool)
        
        if n < lookback:
            return pd.Series(res, index=df.index)
        
        # Find local maxima
        try:
            maxima_idx = argrelextrema(close, np.greater, order=5)[0]
        except:
            return pd.Series(res, index=df.index)
        
        for i in range(len(maxima_idx) - 2):
            left_shoulder = close[maxima_idx[i]]
            head = close[maxima_idx[i + 1]]
            right_shoulder = close[maxima_idx[i + 2]]
            
            # Check if head is higher and shoulders are similar
            if (head > left_shoulder and head > right_shoulder and
                abs(left_shoulder - right_shoulder) / left_shoulder < 0.05):
                if maxima_idx[i + 2] < n:
                    res[maxima_idx[i + 2]:] = True
                    break
        
        return pd.Series(res, index=df.index)
    
    @staticmethod
    def detect_inverse_head_and_shoulders(df, lookback=50):
        """
        Detect inverse head and shoulders pattern
        """
        close = np.asarray(df['Close']).astype(float).ravel()
        n = len(close)
        res = np.zeros(n, dtype=bool)
        
        if n < lookback:
            return pd.Series(res, index=df.index)
        
        # Find local minima
        try:
            minima_idx = argrelextrema(close, np.less, order=5)[0]
        except:
            return pd.Series(res, index=df.index)
        
        for i in range(len(minima_idx) - 2):
            left_shoulder = close[minima_idx[i]]
            head = close[minima_idx[i + 1]]
            right_shoulder = close[minima_idx[i + 2]]
            
            # Check if head is lower and shoulders are similar
            if (head < left_shoulder and head < right_shoulder and
                abs(left_shoulder - right_shoulder) / left_shoulder < 0.05):
                if minima_idx[i + 2] < n:
                    res[minima_idx[i + 2]:] = True
                    break
        
        return pd.Series(res, index=df.index)
    
    @staticmethod
    def detect_trendline_breakout(df, side='up', lookback=30, min_break_pct=0.01):
        """
        Detect trendline breakout
        side: 'up' for upward breakout, 'down' for downward breakout
        """
        closes = np.asarray(df['Close']).astype(float).ravel()
        n = len(closes)
        res = np.zeros(n, dtype=bool)
        
        if n < lookback + 2:
            return pd.Series(res, index=df.index)
        
        for i in range(lookback, n):
            window = closes[i - lookback:i]
            x = np.arange(len(window))
            y = window.astype(float)
            
            # Linear regression
            slope, intercept = np.polyfit(x, y, 1)
            trend_at_last = slope * (len(window) - 1) + intercept
            price = closes[i]
            
            if side == 'up' and price > trend_at_last * (1 + min_break_pct):
                res[i] = True
            elif side == 'down' and price < trend_at_last * (1 - min_break_pct):
                res[i] = True
        
        return pd.Series(res, index=df.index)
    
    @staticmethod
    def detect_triangle_pattern(df, lookback=50):
        """
        Detect triangle consolidation pattern
        """
        high = np.asarray(df['High']).astype(float).ravel()
        low = np.asarray(df['Low']).astype(float).ravel()
        n = len(high)
        res = np.zeros(n, dtype=bool)
        
        if n < lookback:
            return pd.Series(res, index=df.index)
        
        for i in range(lookback, n):
            window_high = high[i - lookback:i]
            window_low = low[i - lookback:i]
            
            # Calculate trend of highs and lows
            x = np.arange(len(window_high))
            high_slope = np.polyfit(x, window_high, 1)[0]
            low_slope = np.polyfit(x, window_low, 1)[0]
            
            # Triangle: highs declining, lows ascending
            if high_slope < 0 and low_slope > 0:
                res[i] = True
        
        return pd.Series(res, index=df.index)
    
    @staticmethod
    def detect_cup_and_handle(df, lookback=100):
        """
        Detect cup and handle pattern
        """
        close = np.asarray(df['Close']).astype(float).ravel()
        n = len(close)
        res = np.zeros(n, dtype=bool)
        
        if n < lookback:
            return pd.Series(res, index=df.index)
        
        for i in range(lookback, n):
            window = close[i - lookback:i]
            
            # Find the cup: U-shaped pattern
            mid = len(window) // 2
            left_max = np.max(window[:mid//2])
            bottom = np.min(window[mid//2:mid+mid//2])
            right_max = np.max(window[-mid//2:])
            
            # Cup condition: similar highs on both sides, lower middle
            if (abs(left_max - right_max) / left_max < 0.05 and
                bottom < left_max * 0.85):
                # Look for handle: slight pullback
                handle = window[-10:]
                if np.max(handle) < right_max * 1.02:
                    res[i] = True
        
        return pd.Series(res, index=df.index)
    
    @staticmethod
    def detect_flag_pattern(df, lookback=20):
        """
        Detect flag pattern (bullish or bearish)
        """
        close = np.asarray(df['Close']).astype(float).ravel()
        n = len(close)
        res = np.zeros(n, dtype=bool)
        
        if n < lookback * 2:
            return pd.Series(res, index=df.index)
        
        for i in range(lookback * 2, n):
            # Look for sharp move (pole)
            pole = close[i - lookback * 2:i - lookback]
            pole_change = (pole[-1] - pole[0]) / pole[0]
            
            # Look for consolidation (flag)
            flag = close[i - lookback:i]
            flag_range = (np.max(flag) - np.min(flag)) / np.mean(flag)
            
            # Flag pattern: strong pole followed by tight consolidation
            if abs(pole_change) > 0.10 and flag_range < 0.05:
                res[i] = True
        
        return pd.Series(res, index=df.index)
    
    @staticmethod
    def detect_wedge_pattern(df, side='rising', lookback=50):
        """
        Detect rising or falling wedge pattern
        """
        high = np.asarray(df['High']).astype(float).ravel()
        low = np.asarray(df['Low']).astype(float).ravel()
        n = len(high)
        res = np.zeros(n, dtype=bool)
        
        if n < lookback:
            return pd.Series(res, index=df.index)
        
        for i in range(lookback, n):
            window_high = high[i - lookback:i]
            window_low = low[i - lookback:i]
            
            x = np.arange(len(window_high))
            high_slope = np.polyfit(x, window_high, 1)[0]
            low_slope = np.polyfit(x, window_low, 1)[0]
            
            if side == 'rising':
                # Rising wedge: both lines ascending, converging
                if high_slope > 0 and low_slope > 0 and low_slope > high_slope * 0.8:
                    res[i] = True
            elif side == 'falling':
                # Falling wedge: both lines descending, converging
                if high_slope < 0 and low_slope < 0 and low_slope < high_slope * 0.8:
                    res[i] = True
        
        return pd.Series(res, index=df.index)
    
    @staticmethod
    def get_all_patterns(df):
        """
        Calculate all chart patterns for a dataframe
        """
        patterns = {}
        
        patterns['Double_Bottom'] = ChartPatterns.detect_double_bottom(df['Close'])
        patterns['Double_Top'] = ChartPatterns.detect_double_top(df['Close'])
        patterns['Head_Shoulders'] = ChartPatterns.detect_head_and_shoulders(df)
        patterns['Inv_Head_Shoulders'] = ChartPatterns.detect_inverse_head_and_shoulders(df)
        patterns['TL_Break_Up'] = ChartPatterns.detect_trendline_breakout(df, 'up')
        patterns['TL_Break_Down'] = ChartPatterns.detect_trendline_breakout(df, 'down')
        patterns['Triangle'] = ChartPatterns.detect_triangle_pattern(df)
        patterns['Cup_Handle'] = ChartPatterns.detect_cup_and_handle(df)
        patterns['Flag'] = ChartPatterns.detect_flag_pattern(df)
        patterns['Rising_Wedge'] = ChartPatterns.detect_wedge_pattern(df, 'rising')
        patterns['Falling_Wedge'] = ChartPatterns.detect_wedge_pattern(df, 'falling')
        
        return patterns
