"""
Scanner Page
Main scanning interface with CSV upload and results display
"""

import streamlit as st
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from modules.scanner_engine import ScannerEngine


def render_scanner_page():
    """Render the scanner page"""
    
    st.markdown('<div class="main-header"><h1>📊 Market Scanner</h1><p>Scan stocks across multiple timeframes with custom workflows</p></div>', unsafe_allow_html=True)
    
    # Get active workflow
    workflow = st.session_state.workflows.get(st.session_state.active_workflow, {})
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Symbol Input")
        
        # Tab for different input methods
        tab1, tab2 = st.tabs(["Manual Entry", "CSV Upload"])
        
        with tab1:
            symbols_input = st.text_area(
                "Enter symbols (comma or newline separated)",
                value="AAPL,MSFT,GOOGL,TSLA,NVDA",
                height=150,
                help="Enter stock symbols separated by commas or new lines"
            )
            
            if st.button("🔄 Load Symbols", key="load_manual_symbols", use_container_width=True):
                # Parse symbols
                symbols = []
                for line in symbols_input.split('\n'):
                    for sym in line.split(','):
                        sym = sym.strip().upper()
                        if sym:
                            symbols.append(sym)
                st.session_state.symbols = list(set(symbols))
                st.success(f"✅ Loaded {len(st.session_state.symbols)} symbols")
        
        with tab2:
            uploaded_file = st.file_uploader(
                "Upload CSV file with symbols",
                type=['csv'],
                help="Upload a CSV file with stock symbols (one per line or in a column)"
            )
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file, header=None)
                    # Try to extract symbols from first column
                    symbols = []
                    for col in df.columns:
                        for val in df[col]:
                            if pd.notna(val):
                                sym = str(val).strip().upper()
                                if sym and len(sym) <= 10:  # Basic validation
                                    symbols.append(sym)
                    
                    symbols = list(set(symbols))
                    st.session_state.symbols = symbols
                    st.success(f"✅ Loaded {len(symbols)} symbols from CSV")
                    st.dataframe(pd.DataFrame({'Symbols': symbols[:20]}), use_container_width=True)
                    if len(symbols) > 20:
                        st.caption(f"... and {len(symbols) - 20} more")
                except Exception as e:
                    st.error(f"❌ Error reading CSV: {e}")
    
    with col2:
        st.subheader("⚙️ Scan Settings")
        
        # Display active workflow info
        st.info(f"**Active Workflow:** {st.session_state.active_workflow}")
        
        with st.expander("📊 Workflow Details", expanded=False):
            st.write("**Indicators:**")
            for ind in workflow.get('indicators', []):
                st.markdown(f"- {ind}")
            
            st.write("**Patterns:**")
            for pat in workflow.get('patterns', []):
                st.markdown(f"- {pat}")
            
            st.write("**Setups:**")
            for setup in workflow.get('setups', []):
                st.markdown(f"- {setup}")
            
            st.write("**Timeframes:**")
            tfs = workflow.get('timeframes', {})
            for tf_name, tf_value in tfs.items():
                st.markdown(f"- **{tf_name}:** {tf_value}")
    
    # Scan button
    st.divider()
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        if st.button("🚀 Run Scan", type="primary", use_container_width=True):
            if not st.session_state.symbols:
                st.error("⚠️ Please load symbols first!")
            else:
                run_scan(workflow)
    
    with col_btn2:
        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.scan_results = None
            st.rerun()
    
    with col_btn3:
        if st.session_state.scan_results is not None:
            csv = st.session_state.scan_results.to_csv(index=False)
            st.download_button(
                label="📥 Export CSV",
                data=csv,
                file_name=f"scan_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Display results
    if st.session_state.scan_results is not None:
        st.divider()
        display_results(st.session_state.scan_results)


def run_scan(workflow):
    """Execute the scan"""
    scanner = ScannerEngine()
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def progress_callback(current, total, symbol):
        progress = current / total
        progress_bar.progress(progress)
        status_text.text(f"Scanning {symbol}... ({current}/{total})")
    
    try:
        with st.spinner("🔄 Scanning markets..."):
            results_df = scanner.scan_multiple_symbols(
                st.session_state.symbols,
                workflow,
                progress_callback
            )
            
            st.session_state.scan_results = results_df
            progress_bar.empty()
            status_text.empty()
            
            if len(results_df) > 0:
                st.success(f"✅ Scan complete! Found {len(results_df)} results")
            else:
                st.warning("⚠️ No results found")
    except Exception as e:
        st.error(f"❌ Error during scan: {e}")
        progress_bar.empty()
        status_text.empty()


def display_results(df):
    """Display scan results in a formatted table"""
    st.subheader("📊 Scan Results")
    
    # Filter out error rows
    error_df = df[df.get('Error').notna()] if 'Error' in df.columns else pd.DataFrame()
    results_df = df[df.get('Error').isna()] if 'Error' in df.columns else df
    
    if len(results_df) == 0:
        st.warning("No results to display")
        return
    
    # Convert string columns to numeric for proper sorting
    if 'Close' in results_df.columns:
        results_df['Close'] = pd.to_numeric(results_df['Close'], errors='coerce')
    
    if 'RSI' in results_df.columns:
        results_df['RSI'] = results_df['RSI'].replace('N/A', float('nan'))
        results_df['RSI'] = pd.to_numeric(results_df['RSI'], errors='coerce')
    
    if 'MACD' in results_df.columns:
        results_df['MACD'] = results_df['MACD'].replace('N/A', float('nan'))
        results_df['MACD'] = pd.to_numeric(results_df['MACD'], errors='coerce')
    
    # Display stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Scanned", len(df))
    
    with col2:
        buy_count = len(results_df[results_df['Signal'] == 'BUY']) if 'Signal' in results_df.columns else 0
        st.metric("Buy Signals", buy_count, delta="Bullish" if buy_count > 0 else None)
    
    with col3:
        sell_count = len(results_df[results_df['Signal'] == 'SELL']) if 'Signal' in results_df.columns else 0
        st.metric("Sell Signals", sell_count, delta="Bearish" if sell_count > 0 else None)
    
    with col4:
        pattern_count = len(results_df[results_df['Patterns'] != '-']) if 'Patterns' in results_df.columns else 0
        st.metric("Patterns Detected", pattern_count)
    
    # Add filters
    st.divider()
    st.subheader("🔍 Filter Results")
    
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        # Signal filter
        signal_options = ['All'] + sorted(results_df['Signal'].unique().tolist()) if 'Signal' in results_df.columns else ['All']
        selected_signal = st.selectbox("Filter by Signal", signal_options, key='signal_filter')
    
    with col_filter2:
        # Pattern filter
        if 'Patterns' in results_df.columns:
            all_patterns = set()
            for patterns_str in results_df['Patterns'].dropna():
                if patterns_str != '-':
                    all_patterns.update([p.strip() for p in str(patterns_str).split(',')])
            pattern_options = ['All', 'Any Pattern', 'No Pattern'] + sorted(list(all_patterns))
        else:
            pattern_options = ['All']
        selected_pattern = st.selectbox("Filter by Pattern", pattern_options, key='pattern_filter')
    
    with col_filter3:
        # Setup filter
        if 'Setups' in results_df.columns:
            all_setups = set()
            for setups_str in results_df['Setups'].dropna():
                if setups_str != '-':
                    all_setups.update([s.strip() for s in str(setups_str).split(',')])
            setup_options = ['All', 'Any Setup', 'No Setup'] + sorted(list(all_setups))
        else:
            setup_options = ['All']
        selected_setup = st.selectbox("Filter by Setup", setup_options, key='setup_filter')
    
    # Apply filters
    filtered_df = results_df.copy()
    
    # Signal filter
    if selected_signal != 'All' and 'Signal' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Signal'] == selected_signal]
    
    # Pattern filter
    if 'Patterns' in filtered_df.columns:
        if selected_pattern == 'Any Pattern':
            filtered_df = filtered_df[filtered_df['Patterns'] != '-']
        elif selected_pattern == 'No Pattern':
            filtered_df = filtered_df[filtered_df['Patterns'] == '-']
        elif selected_pattern != 'All':
            filtered_df = filtered_df[filtered_df['Patterns'].str.contains(selected_pattern, na=False)]
    
    # Setup filter
    if 'Setups' in filtered_df.columns:
        if selected_setup == 'Any Setup':
            filtered_df = filtered_df[filtered_df['Setups'] != '-']
        elif selected_setup == 'No Setup':
            filtered_df = filtered_df[filtered_df['Setups'] == '-']
        elif selected_setup != 'All':
            filtered_df = filtered_df[filtered_df['Setups'].str.contains(selected_setup, na=False)]
    
    # Display filtered count
    st.caption(f"Showing {len(filtered_df)} of {len(results_df)} results")
    
    # Display results table with formatting
    if len(filtered_df) > 0:
        # Configure column display
        column_config = {
            'Close': st.column_config.NumberColumn(
                'Close',
                help='Closing price',
                format='$%.2f'
            ),
            'RSI': st.column_config.NumberColumn(
                'RSI',
                help='Relative Strength Index',
                format='%.2f',
                min_value=0,
                max_value=100
            ),
            'MACD': st.column_config.NumberColumn(
                'MACD',
                help='Moving Average Convergence Divergence',
                format='%.3f'
            )
        }
        
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400,
            column_config=column_config
        )
        
        # Symbol selector for chart view
        st.divider()
        col_select1, col_select2 = st.columns([3, 1])
        
        with col_select1:
            selected_symbol = st.selectbox(
                "Select symbol to view detailed chart:",
                filtered_df['Symbol'].tolist() if 'Symbol' in filtered_df.columns else [],
                key='chart_symbol_select'
            )
        
        with col_select2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("📈 View Chart →", use_container_width=True):
                st.session_state.selected_chart_symbol = selected_symbol
                st.success(f"✅ Selected {selected_symbol}. Go to the Charts page to view details.")
    else:
        st.info("No results match the selected filters. Try adjusting the filters above.")
    
    # Display errors if any
    if len(error_df) > 0:
        with st.expander(f"⚠️ Errors ({len(error_df)})", expanded=False):
            st.dataframe(error_df, use_container_width=True)
