# Advanced Market Scanner - Complete Application

A comprehensive, production-ready Streamlit application for advanced stock market scanning with multi-timeframe analysis, technical indicators, chart patterns, and custom workflows.

## 🎯 Features

### Core Functionality
- **Multi-Page Interface**: Scanner, Charts, Configuration, Workflows
- **13+ Technical Indicators**: Yoda, RSI, MACD, Bollinger Bands, ADX, and more
- **11+ Chart Patterns**: Double tops/bottoms, H&S, trendline breaks, triangles, etc.
- **Multi-Timeframe Analysis**: Wave (4h), Tide (1d), SuperTide (1wk)
- **Custom Workflows**: Create, save, and manage scanning strategies
- **Interactive Charts**: TradingView-style charts with Plotly
- **CSV Upload**: Bulk symbol import
- **Export Results**: Download scan results as CSV

### Advanced Features
- Custom indicator support (Python code)
- Custom pattern detection
- Complex AND/OR rule logic
- Visual rule builder
- Workflow import/export (JSON)
- Real-time progress tracking

## 📦 Installation

### Requirements
- Python 3.8 or higher
- Internet connection (for market data)

### Quick Install

```bash
# Clone or download the files
cd complete_scanner

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run scanner_main.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🚀 Quick Start

### 1. First Run
```bash
streamlit run scanner_main.py
```

### 2. Load Symbols
- Go to Scanner page
- Upload a CSV file with stock symbols OR
- Enter symbols manually: `AAPL,MSFT,GOOGL,TSLA,NVDA`
- Click "Load Symbols"

### 3. Run Scan
- Select or create a workflow
- Click "🚀 Run Scan"
- View results in the table
- Export to CSV if needed

### 4. View Charts
- Select a symbol from scan results
- Go to Charts page
- Load detailed technical analysis
- View multi-timeframe indicators

### 5. Customize
- Go to Configuration page to add custom indicators/patterns
- Go to Workflows page to create custom strategies
- Mix and match indicators, patterns, and setups

## 📁 Project Structure

```
complete_scanner/
├── scanner_main.py          # Main application entry point
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── nasdaq100.csv            # Sample watchlist
│
├── modules/                 # Core functionality
│   ├── __init__.py
│   ├── indicators.py        # Technical indicators library
│   ├── patterns.py          # Chart pattern detection
│   ├── rule_engine.py       # Complex rule evaluation
│   └── scanner_engine.py    # Main scanning logic
│
└── pages/                   # Streamlit pages
    ├── __init__.py
    ├── scanner.py           # Scanner interface
    ├── charts.py            # Chart visualization
    ├── configuration.py     # Settings & customization
    └── workflows.py         # Workflow management
```

## 📊 Usage Examples

### Example 1: Scan NASDAQ 100
```python
1. Upload nasdaq100.csv
2. Select "Default Scanner" workflow
3. Click "Run Scan"
4. View BUY/SELL signals
5. Export results
```

### Example 2: Create Custom Workflow
```python
1. Go to Workflows page
2. Click "Create New Workflow"
3. Name: "Momentum Strategy"
4. Select: RSI, MACD, ADX
5. Select patterns: TL_Break_Up
6. Save and activate
7. Run scan with new workflow
```

### Example 3: Add Custom Indicator
```python
1. Go to Configuration → Indicators
2. Click "Add New Custom Indicator"
3. Name: "Price ROC"
4. Code:
   def calculate(df, period=14):
       return df['Close'].pct_change(period) * 100
5. Save and use in workflows
```

## 🎨 Key Components

### Indicators Library (13+)
- **Yoda**: Custom MACD + SMA + TTM Squeeze
- **RSI**: Relative Strength Index
- **MACD**: Moving Average Convergence Divergence
- **Bollinger Bands**: Volatility bands
- **ADX**: Trend strength
- **Stochastic**: Momentum oscillator
- **ATR**: Average True Range
- **EMA**: 5, 20, 50 periods
- **SMA**: 200 period
- **OBV**: On Balance Volume
- **VWAP**: Volume Weighted Average Price

### Chart Patterns (11+)
- Double Bottom/Top (reversal)
- Head & Shoulders (reversal)
- Trendline Breakouts (breakout)
- Triangle (consolidation)
- Cup & Handle (continuation)
- Flag (continuation)
- Rising/Falling Wedge (reversal)

### Trading Setups
- **Momentum Long**: Multi-timeframe bullish alignment
- **Momentum Short**: Multi-timeframe bearish alignment
- **Breakout**: Pattern-based breakout strategy

## 🔧 Configuration

### Multi-Timeframe Setup
The scanner uses a hierarchical timeframe approach:
- **Wave (4h)**: Short-term entry signals
- **Tide (1d)**: Medium-term trend confirmation
- **SuperTide (1wk)**: Long-term trend direction

### Workflow Configuration
Each workflow can include:
- List of indicators to calculate
- List of patterns to detect
- List of setups to evaluate
- Custom timeframe intervals

### Custom Code Support
Add your own indicators and patterns using Python:

```python
# Custom Indicator Example
def calculate(df, period=20):
    """Calculate custom momentum"""
    return df['Close'].pct_change(period) * 100

# Custom Pattern Example
def detect(df, lookback=50):
    """Detect custom pattern"""
    close = df['Close'].values
    pattern = np.zeros(len(close), dtype=bool)
    # Your logic here
    return pd.Series(pattern, index=df.index)
```

## 📈 Data Source

Market data is provided by **Yahoo Finance** via the `yfinance` library:
- Real-time quotes
- Historical OHLC data
- Volume data
- Multiple timeframe support

## 🎓 Tips & Best Practices

1. **Start Simple**: Use the default workflow first
2. **One Strategy**: Create one workflow per trading strategy
3. **Backtest**: Review historical signals on charts
4. **Multi-Timeframe**: Always check Wave, Tide, SuperTide alignment
5. **Volume**: Use volume indicators for confirmation
6. **Export Data**: Save scan results for analysis
7. **Custom Indicators**: Add indicators specific to your strategy
8. **Regular Updates**: Update watchlists regularly

## 🐛 Troubleshooting

### Application won't start
```bash
pip install -r requirements.txt --upgrade
streamlit run scanner_main.py
```

### No data for symbol
- Check symbol format (use Yahoo Finance symbols)
- Try different timeframe
- Verify internet connection

### Slow performance
- Reduce number of symbols (scan 50 at a time)
- Use daily timeframe instead of intraday
- Disable unused indicators

### Pattern not detected
- Patterns need specific market conditions
- Check if enough historical data available
- Review pattern definition in Configuration

## 📚 Additional Resources

### Documentation
- `README.md` - This file (installation & usage)
- Configuration page - Indicator/pattern details
- Code comments - Technical documentation

### Example Files
- `nasdaq100.csv` - Sample watchlist (100 symbols)
- Default workflows - Pre-configured strategies
- Example indicators - In Configuration page

## ⚖️ Disclaimer

**IMPORTANT**: This tool is for educational purposes only.

- NOT financial advice
- Use at your own risk
- Past performance ≠ future results
- Always do your own research
- Consider consulting a financial advisor

## 🤝 Support

For questions or issues:
- Check code comments
- Review Configuration page
- Inspect module docstrings

## 📝 Version

**Version**: 2.0 - Complete Implementation
**Released**: November 2025
**Python**: 3.8+
**License**: Educational Use

## 🎉 Getting Started

Ready to scan? Run:

```bash
streamlit run scanner_main.py
```

Upload your watchlist, select a workflow, and start scanning!

---

**Happy Trading! 📈**

(Remember: This is educational software, not financial advice)
