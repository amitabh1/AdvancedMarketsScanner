# 📝 CHANGELOG - Advanced Market Scanner

## Version 2.1 - November 4, 2025

### 🎉 New Features

#### Scanner Results Filtering
- **Signal Filter**: Filter results by BUY, SELL, or NEUTRAL signals
- **Pattern Filter**: Filter by specific chart patterns or "Any Pattern"/"No Pattern"
- **Setup Filter**: Filter by trading setups or "Any Setup"/"No Setup"
- **Live Filter Count**: Shows "Showing X of Y results" as you filter

#### Improved Data Display
- **Numeric Columns**: RSI, MACD, and Close are now numeric for proper sorting
- **Column Formatting**: 
  - Close displayed as currency ($XX.XX)
  - RSI formatted to 2 decimals (0-100 range)
  - MACD formatted to 3 decimals
- **Sortable Columns**: Click column headers to sort by any field

### 🔧 Bug Fixes

#### Import Error Fixed (v2.0)
- Fixed `ModuleNotFoundError: No module named 'pages'`
- Added proper Python path handling in scanner_main.py
- Added comprehensive error messages

#### Charts KeyError Fixed (v2.0)
- Fixed `KeyError: 'MACD_Signal'` in charts.py
- Added column existence checks before plotting
- Shows helpful messages when indicators not calculated

#### Data Type Issues Fixed (v2.1)
- RSI, MACD, Close now properly numeric in results
- Removed "N/A" strings, replaced with None/NaN
- Proper sorting now works on numeric columns

### 🎨 UI Improvements

- Added 3-column filter interface
- Improved filter dropdowns with "All", "Any", "No" options
- Better filter result display
- Symbol selector now uses filtered results
- Cleaner layout with dividers

### 📊 Technical Changes

#### scanner.py
- Added filter UI components (3 selectboxes)
- Added filter logic for Signal, Patterns, Setups
- Converted string columns to numeric with pd.to_numeric()
- Added st.column_config for better number formatting
- Added filtered count display

#### scanner_engine.py
- Changed RSI from f"{rsi:.2f}" to float(rsi)
- Changed MACD from f"{macd:.2f}" to float(macd)
- Now returns None instead of 'N/A' for missing values
- Close always returned as float

### 📚 Documentation Updates

- Updated README with new filter features
- Added screenshots of filter interface (coming soon)
- Updated QUICK_START guide

---

## Version 2.0 - November 4, 2025

### Initial Release
- Complete Streamlit application
- 13+ technical indicators
- 11+ chart patterns
- Multi-timeframe analysis
- Interactive charts
- Custom workflows
- CSV import/export

---

## Migration Guide

### From v2.0 to v2.1

No breaking changes! Simply:
1. Extract new ZIP file
2. Run `pip install -r requirements.txt` (no new dependencies)
3. Run application as usual

Your existing workflows and data will work without changes.

---

## Roadmap

### Coming Soon (v2.2)
- [ ] Export filtered results to CSV
- [ ] Save filter presets
- [ ] Advanced filter combinations (AND/OR logic)
- [ ] Custom filter rules

### Future (v3.0)
- [ ] Backtesting framework
- [ ] Strategy performance metrics
- [ ] Alert system
- [ ] Portfolio tracking

---

## Support

For issues or questions:
- See docs/TROUBLESHOOTING.md
- Run python check_setup.py
- Check docs/QUICK_FIX.md

---

**Current Version**: 2.1  
**Release Date**: November 4, 2025  
**Status**: Production Ready ✅
