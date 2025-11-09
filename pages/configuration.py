"""
Configuration Page
Configure indicators, patterns, setups and rules
"""

import streamlit as st


def render_configuration_page():
    """Render the configuration page"""
    
    st.markdown('<div class="main-header"><h1>⚙️ Configuration</h1><p>Configure indicators, patterns, and trading setups</p></div>', unsafe_allow_html=True)
    
    # Tabs for different configuration sections
    tab1, tab2, tab3 = st.tabs([
        "📊 Indicators",
        "📐 Chart Patterns",
        "🎯 Setups & Rules"
    ])
    
    with tab1:
        render_indicators_config()
    
    with tab2:
        render_patterns_config()
    
    with tab3:
        render_setups_config()


def render_indicators_config():
    """Configure indicators"""
    
    st.subheader("📊 Indicator Library")
    
    st.write("### Standard Indicators")
    
    # Standard indicators information
    indicators_info = {
        'Yoda': 'Combined MACD + SMA + TTM Squeeze indicator (custom)',
        'RSI': 'Relative Strength Index (14-period)',
        'MACD': 'Moving Average Convergence Divergence',
        'BB': 'Bollinger Bands (20-period, 2 std dev)',
        'ATR': 'Average True Range (14-period)',
        'ADX': 'Average Directional Index (trend strength)',
        'Stochastic': 'Stochastic Oscillator (%K, %D)',
        'OBV': 'On Balance Volume',
        'VWAP': 'Volume Weighted Average Price',
        'EMA_5': 'Exponential Moving Average (5-period)',
        'EMA_20': 'Exponential Moving Average (20-period)',
        'EMA_50': 'Exponential Moving Average (50-period)',
        'SMA_200': 'Simple Moving Average (200-period)'
    }
    
    for indicator, description in indicators_info.items():
        with st.expander(f"**{indicator}**"):
            st.write(description)
            st.code(f"Usage in workflow: indicators = ['{indicator}']", language='python')
    
    st.divider()
    
    # Custom indicators
    st.write("### Custom Indicators")
    st.info("💡 Add your own custom indicators using Python code")
    
    # List custom indicators
    if st.session_state.custom_indicators:
        st.write("#### Your Custom Indicators")
        for name, code in st.session_state.custom_indicators.items():
            with st.expander(f"📊 {name}"):
                st.code(code, language='python')
                if st.button(f"Delete {name}", key=f"del_ind_{name}"):
                    del st.session_state.custom_indicators[name]
                    st.rerun()
    
    # Add new custom indicator
    with st.expander("➕ Add New Custom Indicator", expanded=False):
        st.write("Create a custom indicator function")
        
        indicator_name = st.text_input(
            "Indicator Name",
            placeholder="MyCustomIndicator",
            help="Enter a unique name for your indicator"
        )
        
        indicator_code = st.text_area(
            "Python Code",
            value="""def calculate(df, period=14):
    '''
    Calculate custom indicator
    Args:
        df: DataFrame with OHLC data
        period: Lookback period
    Returns:
        Series with indicator values
    '''
    # Your calculation here
    result = df['Close'].rolling(period).mean()
    return result""",
            height=300,
            help="Write a function that takes a DataFrame and returns indicator values"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("💾 Save Indicator", use_container_width=True):
                if indicator_name and indicator_code:
                    st.session_state.custom_indicators[indicator_name] = indicator_code
                    st.success(f"✅ Saved {indicator_name}")
                    st.rerun()
                else:
                    st.error("Please provide both name and code")
        
        with col2:
            if st.button("🧪 Test Indicator Code", use_container_width=True):
                try:
                    compile(indicator_code, '<string>', 'exec')
                    st.success("✅ Code syntax is valid")
                except SyntaxError as e:
                    st.error(f"❌ Syntax Error: {e}")


def render_patterns_config():
    """Configure chart patterns"""
    
    st.subheader("📐 Chart Pattern Library")
    
    st.write("### Standard Patterns")
    
    # Standard patterns
    patterns_info = {
        'Double_Bottom': 'Two consecutive lows at similar price levels - Bullish reversal',
        'Double_Top': 'Two consecutive highs at similar price levels - Bearish reversal',
        'Head_Shoulders': 'Three peaks with middle peak highest - Bearish reversal',
        'Inv_Head_Shoulders': 'Three troughs with middle trough lowest - Bullish reversal',
        'TL_Break_Up': 'Price breaks above resistance trendline - Bullish',
        'TL_Break_Down': 'Price breaks below support trendline - Bearish',
        'Triangle': 'Price consolidation pattern - Breakout pending',
        'Cup_Handle': 'U-shaped pattern with handle - Bullish continuation',
        'Flag': 'Sharp move followed by consolidation - Continuation',
        'Rising_Wedge': 'Converging trendlines trending up - Bearish',
        'Falling_Wedge': 'Converging trendlines trending down - Bullish'
    }
    
    for pattern, description in patterns_info.items():
        with st.expander(f"**{pattern}**"):
            st.write(description)
            st.code(f"Usage: patterns = ['{pattern}']", language='python')
    
    st.divider()
    
    # Custom patterns
    st.write("### Custom Patterns")
    st.info("💡 Add your own pattern detection algorithms")
    
    # List custom patterns
    if st.session_state.custom_patterns:
        st.write("#### Your Custom Patterns")
        for name, code in st.session_state.custom_patterns.items():
            with st.expander(f"📐 {name}"):
                st.code(code, language='python')
                if st.button(f"Delete {name}", key=f"del_pat_{name}"):
                    del st.session_state.custom_patterns[name]
                    st.rerun()
    
    # Add new custom pattern
    with st.expander("➕ Add New Custom Pattern", expanded=False):
        pattern_name = st.text_input(
            "Pattern Name",
            placeholder="MyCustomPattern",
            help="Enter a unique name for your pattern"
        )
        
        pattern_code = st.text_area(
            "Python Code",
            value="""def detect(df, lookback=50):
    '''
    Detect custom pattern
    Args:
        df: DataFrame with OHLC data
        lookback: Lookback period for pattern detection
    Returns:
        Series of boolean values indicating pattern presence
    '''
    import numpy as np
    import pandas as pd
    
    # Your pattern detection logic here
    close = df['Close'].values
    pattern = np.zeros(len(close), dtype=bool)
    
    # Example: simple pattern detection
    for i in range(lookback, len(close)):
        window = close[i-lookback:i]
        # Add your pattern logic here
        if np.max(window) == window[-1]:
            pattern[i] = True
    
    return pd.Series(pattern, index=df.index)""",
            height=400
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("💾 Save Pattern", use_container_width=True):
                if pattern_name and pattern_code:
                    st.session_state.custom_patterns[pattern_name] = pattern_code
                    st.success(f"✅ Saved {pattern_name}")
                    st.rerun()
                else:
                    st.error("Please provide both name and code")
        
        with col2:
            if st.button("🧪 Test Pattern Code", use_container_width=True):
                try:
                    compile(pattern_code, '<string>', 'exec')
                    st.success("✅ Code syntax is valid")
                except SyntaxError as e:
                    st.error(f"❌ Syntax Error: {e}")


def render_setups_config():
    """Configure trading setups"""
    
    st.subheader("🎯 Trading Setups & Rules")
    
    st.write("### Predefined Setups")
    
    # Standard setups
    setups_info = {
        'Momentum_Long': {
            'description': 'Multi-timeframe bullish momentum alignment',
            'conditions': [
                'Wave: RSI > 50 AND MACD > 0',
                'Tide: Buy Signal AND Close > SMA',
                'SuperTide: Close > SMA OR TTM Fired'
            ]
        },
        'Momentum_Short': {
            'description': 'Multi-timeframe bearish momentum alignment',
            'conditions': [
                'Wave: RSI < 50 AND MACD < 0',
                'Tide: Sell Signal AND Close < SMA',
                'SuperTide: Close < SMA OR TTM Fired'
            ]
        },
        'Breakout': {
            'description': 'Price breakout with pattern confirmation',
            'conditions': [
                'Wave: TL Break Up OR Double Bottom',
                'Tide: RSI between 40 and 70'
            ]
        }
    }
    
    for setup_name, setup_info in setups_info.items():
        with st.expander(f"**{setup_name}**"):
            st.write(f"**Description:** {setup_info['description']}")
            st.write("**Conditions:**")
            for condition in setup_info['conditions']:
                st.markdown(f"- {condition}")
            st.code(f"Usage: setups = ['{setup_name}']", language='python')
    
    st.divider()
    
    # Rule examples
    st.write("### Rule Examples")
    
    rule_examples = {
        'Momentum Bullish': 'RSI > 50 AND MACD > 0 AND ADX > 20',
        'Oversold Bounce': 'RSI < 30 AND Price > BB_Lower',
        'Breakout Confirmation': 'Close > SMA_200 AND Volume > AVG_Volume * 1.5',
        'Trend Following': 'EMA_20 > EMA_50 AND ADX > 25',
    }
    
    for rule, description in rule_examples.items():
        with st.expander(f"📋 {rule}"):
            st.code(description, language='text')
            st.caption("Use these patterns to create your own setups")
