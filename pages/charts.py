"""
Charts Page
Interactive TradingView-style charts with detailed analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from modules.scanner_engine import ScannerEngine


def render_charts_page():
    """Render the charts page"""
    
    st.markdown('<div class="main-header"><h1>📈 Advanced Charts</h1><p>Detailed technical analysis with multi-timeframe view</p></div>', unsafe_allow_html=True)
    
    # Symbol selector
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Check if symbol was selected from scanner
        default_symbol = st.session_state.get('selected_chart_symbol', 'AAPL')
        
        symbol = st.text_input(
            "Enter Symbol",
            value=default_symbol,
            help="Enter a stock symbol to analyze"
        ).upper()
    
    with col2:
        timeframe_display = st.selectbox(
            "Primary Timeframe",
            ["Wave (4h)", "Tide (1d)", "SuperTide (1wk)"],
            index=1
        )
        
        # Map display name to actual timeframe
        tf_map = {
            "Wave (4h)": "4h",
            "Tide (1d)": "1d",
            "SuperTide (1wk)": "1wk"
        }
        timeframe = tf_map[timeframe_display]
    
    with col3:
        if st.button("🔄 Load Chart", type="primary", use_container_width=True):
            st.session_state.chart_symbol = symbol
            st.session_state.chart_timeframe = timeframe
            st.rerun()
    
    # Load and display chart
    if 'chart_symbol' in st.session_state:
        load_and_display_chart(
            st.session_state.chart_symbol,
            st.session_state.get('chart_timeframe', '1d')
        )


def load_and_display_chart(symbol, timeframe):
    """Load data and display comprehensive charts"""
    
    scanner = ScannerEngine()
    
    with st.spinner(f"📊 Loading data for {symbol}..."):
        # Download data
        df = scanner.download_data(symbol, timeframe, period='6mo')
        
        if df is None or len(df) == 0:
            st.error(f"❌ Could not load data for {symbol}")
            return
        
        # Get active workflow
        workflow = st.session_state.workflows.get(st.session_state.active_workflow, {})
        
        # Calculate indicators
        df = scanner.calculate_indicators(df, workflow.get('indicators', ['Yoda', 'RSI', 'MACD']))
        df = scanner.calculate_patterns(df, workflow.get('patterns', []))
        
        # Display metrics
        display_metrics(df, symbol)
        
        # Display charts
        st.divider()
        display_main_chart(df, symbol, timeframe)
        
        # Display indicator charts
        st.divider()
        display_indicator_charts(df, symbol)
        
        # Display signals table
        st.divider()
        display_signals_table(df, symbol)
        
        # Multi-timeframe analysis
        st.divider()
        display_multi_timeframe_analysis(symbol, workflow)


def display_metrics(df, symbol):
    """Display key metrics"""
    
    st.subheader(f"📊 {symbol} - Key Metrics")
    
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        price_change = last['Close'] - prev['Close']
        price_pct = (price_change / prev['Close']) * 100
        st.metric(
            "Price",
            f"${last['Close']:.2f}",
            f"{price_pct:+.2f}%",
            delta_color="normal"
        )
    
    with col2:
        if 'RSI' in df.columns:
            rsi = last['RSI']
            st.metric(
                "RSI",
                f"{rsi:.2f}",
                "Overbought" if rsi > 70 else ("Oversold" if rsi < 30 else "Normal"),
                delta_color="off"
            )
    
    with col3:
        if 'MACD' in df.columns:
            macd = last['MACD']
            st.metric(
                "MACD",
                f"{macd:.3f}",
                "Bullish" if macd > 0 else "Bearish",
                delta_color="normal" if macd > 0 else "inverse"
            )
    
    with col4:
        if 'ADX' in df.columns:
            adx = last['ADX']
            trend_strength = "Strong" if adx > 25 else ("Moderate" if adx > 20 else "Weak")
            st.metric("ADX", f"{adx:.2f}", trend_strength, delta_color="off")
    
    with col5:
        if 'ATR' in df.columns:
            atr = last['ATR']
            st.metric("ATR", f"{atr:.2f}", "Volatility", delta_color="off")


def display_main_chart(df, symbol, timeframe):
    """Display main candlestick chart with overlays"""
    
    st.subheader(f"💹 {symbol} - Candlestick Chart ({timeframe})")
    
    # Create subplots: main chart + volume
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(f'{symbol} Price', 'Volume')
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ),
        row=1, col=1
    )
    
    # Add SMA if available
    if 'SMA' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['SMA'],
                name='SMA(50)',
                line=dict(color='orange', width=2)
            ),
            row=1, col=1
        )
    
    # Add EMA if available
    if 'EMA_20' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['EMA_20'],
                name='EMA(20)',
                line=dict(color='blue', width=1.5, dash='dot')
            ),
            row=1, col=1
        )
    
    # Add Bollinger Bands if available
    if all(col in df.columns for col in ['BB_Upper', 'BB_Middle', 'BB_Lower']):
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['BB_Upper'],
                name='BB Upper',
                line=dict(color='rgba(250, 128, 114, 0.5)', width=1),
                fill=None
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['BB_Lower'],
                name='BB Lower',
                line=dict(color='rgba(173, 216, 230, 0.5)', width=1),
                fill='tonexty',
                fillcolor='rgba(173, 216, 230, 0.2)'
            ),
            row=1, col=1
        )
    
    # Mark Buy/Sell signals
    if 'Buy_Signal' in df.columns:
        buy_signals = df[df['Buy_Signal'] == True]
        if len(buy_signals) > 0:
            fig.add_trace(
                go.Scatter(
                    x=buy_signals.index,
                    y=buy_signals['Low'] * 0.995,
                    mode='markers',
                    name='Buy Signal',
                    marker=dict(
                        symbol='triangle-up',
                        size=15,
                        color='green',
                        line=dict(width=2, color='darkgreen')
                    )
                ),
                row=1, col=1
            )
    
    if 'Sell_Signal' in df.columns:
        sell_signals = df[df['Sell_Signal'] == True]
        if len(sell_signals) > 0:
            fig.add_trace(
                go.Scatter(
                    x=sell_signals.index,
                    y=sell_signals['High'] * 1.005,
                    mode='markers',
                    name='Sell Signal',
                    marker=dict(
                        symbol='triangle-down',
                        size=15,
                        color='red',
                        line=dict(width=2, color='darkred')
                    )
                ),
                row=1, col=1
            )
    
    # Volume bars
    colors = ['red' if df['Close'].iloc[i] < df['Open'].iloc[i] else 'green' 
              for i in range(len(df))]
    
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.5
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        height=800,
        template='plotly_dark',
        xaxis_rangeslider_visible=False,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
    
    st.plotly_chart(fig, use_container_width=True)


def display_indicator_charts(df, symbol):
    """Display indicator charts"""
    
    st.subheader("📊 Technical Indicators")
    
    tab1, tab2, tab3 = st.tabs(["RSI & Stochastic", "MACD", "Volume Indicators"])
    
    with tab1:
        if 'RSI' in df.columns or 'Stoch_K' in df.columns:
            fig = make_subplots(
                rows=2, cols=1,
                row_heights=[0.5, 0.5],
                shared_xaxes=True,
                subplot_titles=('RSI', 'Stochastic')
            )
            
            # RSI
            if 'RSI' in df.columns:
                fig.add_trace(
                    go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple', width=2)),
                    row=1, col=1
                )
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=1, col=1, annotation_text="Overbought")
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=1, col=1, annotation_text="Oversold")
            
            # Stochastic if available
            if 'Stoch_K' in df.columns and 'Stoch_D' in df.columns:
                fig.add_trace(
                    go.Scatter(x=df.index, y=df['Stoch_K'], name='%K', line=dict(color='blue')),
                    row=2, col=1
                )
                fig.add_trace(
                    go.Scatter(x=df.index, y=df['Stoch_D'], name='%D', line=dict(color='orange')),
                    row=2, col=1
                )
                fig.add_hline(y=80, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=20, line_dash="dash", line_color="green", row=2, col=1)
            
            fig.update_layout(height=500, template='plotly_dark', showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("💡 RSI or Stochastic indicators not calculated. Add them to your workflow to view this chart.")
    
    with tab2:
        if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue', width=2)))
            fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name='Signal', line=dict(color='orange', width=2)))
            
            # Histogram
            if 'MACD_Hist' in df.columns:
                colors = ['green' if val >= 0 else 'red' for val in df['MACD_Hist']]
                fig.add_trace(go.Bar(x=df.index, y=df['MACD_Hist'], name='Histogram', marker_color=colors, opacity=0.5))
            
            fig.add_hline(y=0, line_dash="dash", line_color="white")
            fig.update_layout(height=400, template='plotly_dark', title='MACD Indicator')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("💡 MACD indicator not calculated. Add 'MACD' to your workflow to view this chart.")
    
    with tab3:
        if 'OBV' in df.columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['OBV'], name='OBV', line=dict(color='cyan', width=2)))
            fig.update_layout(height=300, template='plotly_dark', title='On Balance Volume (OBV)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("💡 OBV indicator not calculated. Add 'OBV' to your workflow to view this chart.")


def display_signals_table(df, symbol):
    """Display detected signals in a table"""
    
    st.subheader("🎯 Detected Signals & Patterns")
    
    # Find all signals
    signals = []
    
    for idx in range(len(df)):
        row = df.iloc[idx]
        date = df.index[idx]
        
        # Check for buy/sell signals
        if 'Buy_Signal' in df.columns and row['Buy_Signal']:
            signals.append({
                'Date': date,
                'Type': 'Buy Signal',
                'Price': row['Close'],
                'Direction': '🟢 Long',
                'Confidence': 'High' if 'RSI' in df.columns and row['RSI'] < 70 else 'Medium'
            })
        
        if 'Sell_Signal' in df.columns and row['Sell_Signal']:
            signals.append({
                'Date': date,
                'Type': 'Sell Signal',
                'Price': row['Close'],
                'Direction': '🔴 Short',
                'Confidence': 'High' if 'RSI' in df.columns and row['RSI'] > 30 else 'Medium'
            })
        
        # Check for patterns
        pattern_cols = ['Double_Bottom', 'Double_Top', 'TL_Break_Up', 'TL_Break_Down']
        for pat in pattern_cols:
            if pat in df.columns and row[pat]:
                signals.append({
                    'Date': date,
                    'Type': pat.replace('_', ' '),
                    'Price': row['Close'],
                    'Direction': '🟢 Long' if 'Bottom' in pat or 'Up' in pat else '🔴 Short',
                    'Confidence': 'Medium'
                })
    
    if signals:
        signals_df = pd.DataFrame(signals).tail(20)  # Show last 20 signals
        st.dataframe(signals_df, use_container_width=True)
    else:
        st.info("No signals detected in the current timeframe")


def display_multi_timeframe_analysis(symbol, workflow):
    """Display multi-timeframe analysis"""
    
    st.subheader("🕐 Multi-Timeframe Analysis")
    
    scanner = ScannerEngine()
    timeframes = workflow.get('timeframes', {'Wave': '4h', 'Tide': '1d', 'SuperTide': '1wk'})
    
    cols = st.columns(len(timeframes))
    
    for idx, (tf_name, tf_interval) in enumerate(timeframes.items()):
        with cols[idx]:
            with st.spinner(f"Loading {tf_name}..."):
                df = scanner.download_data(symbol, tf_interval, period='6mo')
                
                if df is not None and len(df) > 0:
                    df = scanner.calculate_indicators(df, ['Yoda', 'RSI'])
                    last = df.iloc[-1]
                    
                    # Determine trend
                    trend = "Neutral"
                    trend_color = "gray"
                    
                    if 'Buy_Signal' in df.columns and last['Buy_Signal']:
                        trend = "Bullish"
                        trend_color = "green"
                    elif 'Sell_Signal' in df.columns and last['Sell_Signal']:
                        trend = "Bearish"
                        trend_color = "red"
                    elif 'Close' in df.columns and 'SMA' in df.columns:
                        if last['Close'] > last['SMA']:
                            trend = "Bullish"
                            trend_color = "green"
                        elif last['Close'] < last['SMA']:
                            trend = "Bearish"
                            trend_color = "red"
                    
                    st.markdown(f"### {tf_name}")
                    st.markdown(f"**Timeframe:** {tf_interval}")
                    st.markdown(f"**Trend:** :{trend_color}[{trend}]")
                    
                    if 'RSI' in df.columns:
                        rsi = last['RSI']
                        st.metric("RSI", f"{rsi:.2f}")
                    
                    if 'Close' in df.columns:
                        st.metric("Close", f"${last['Close']:.2f}")
                else:
                    st.error(f"No data for {tf_name}")
