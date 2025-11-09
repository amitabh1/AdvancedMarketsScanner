"""
Advanced Market Scanner - Main Application
Multi-timeframe stock scanner with custom workflows
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set page config FIRST before any other Streamlit commands
st.set_page_config(
    page_title="Advanced Market Scanner",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'symbols' not in st.session_state:
    st.session_state.symbols = []
    
if 'scan_results' not in st.session_state:
    st.session_state.scan_results = None
    
if 'workflows' not in st.session_state:
    st.session_state.workflows = {
        'Default Scanner': {
            'indicators': ['Yoda', 'RSI', 'MACD'],
            'patterns': ['Double_Bottom', 'Double_Top', 'TL_Break_Up'],
            'setups': ['Momentum_Long'],
            'timeframes': {'Wave': '4h', 'Tide': '1d', 'SuperTide': '1wk'}
        }
    }
    
if 'active_workflow' not in st.session_state:
    st.session_state.active_workflow = 'Default Scanner'
    
if 'custom_indicators' not in st.session_state:
    st.session_state.custom_indicators = {}
    
if 'custom_patterns' not in st.session_state:
    st.session_state.custom_patterns = {}
    
if 'custom_setups' not in st.session_state:
    st.session_state.custom_setups = {}
    
if 'selected_chart_symbol' not in st.session_state:
    st.session_state.selected_chart_symbol = 'AAPL'

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .signal-bullish {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    
    .signal-bearish {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .workflow-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: #667eea;
        color: white;
        border-radius: 15px;
        font-size: 0.85rem;
        margin: 0.25rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("# 🔍 Market Scanner")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["📊 Scanner", "📈 Charts", "⚙️ Configuration", "🔧 Workflows"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Workflow selector
    st.subheader("Active Workflow")
    workflow_name = st.selectbox(
        "Select Workflow",
        list(st.session_state.workflows.keys()),
        key='workflow_selector'
    )
    st.session_state.active_workflow = workflow_name
    
    workflow = st.session_state.workflows[workflow_name]
    st.caption(f"🎯 Indicators: {len(workflow['indicators'])}")
    st.caption(f"📐 Patterns: {len(workflow['patterns'])}")
    st.caption(f"🎪 Setups: {len(workflow['setups'])}")
    
    st.markdown("---")
    st.caption("v2.0 - Advanced Market Scanner")
    st.caption("Data: Yahoo Finance")

# Import page modules with error handling
try:
    from pages.scanner import render_scanner_page
    from pages.charts import render_charts_page
    from pages.configuration import render_configuration_page
    from pages.workflows import render_workflows_page
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.error("**Troubleshooting Steps:**")
    st.code("""
# 1. Make sure you're in the correct directory:
cd /path/to/your/scanner/folder

# 2. Verify directory structure:
ls -la

# You should see:
# scanner_main.py
# modules/
# pages/
# requirements.txt

# 3. Check Python path:
import sys
print(sys.path)

# 4. Run application:
streamlit run scanner_main.py
    """, language='bash')
    
    with st.expander("📁 Expected Directory Structure"):
        st.code("""
your_folder/
├── scanner_main.py
├── requirements.txt
├── modules/
│   ├── __init__.py
│   ├── indicators.py
│   ├── patterns.py
│   ├── rule_engine.py
│   └── scanner_engine.py
└── pages/
    ├── __init__.py
    ├── scanner.py
    ├── charts.py
    ├── configuration.py
    └── workflows.py
        """)
    st.stop()

# Main content based on page selection
if page == "📊 Scanner":
    render_scanner_page()
    
elif page == "📈 Charts":
    render_charts_page()
    
elif page == "⚙️ Configuration":
    render_configuration_page()
    
elif page == "🔧 Workflows":
    render_workflows_page()
