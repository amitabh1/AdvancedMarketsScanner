# 🔧 Troubleshooting Guide - Advanced Market Scanner

## ❌ Common Error: ModuleNotFoundError: No module named 'pages'

### Quick Fix (Choose One):

#### Solution 1: Run from Correct Directory (Recommended)
```bash
# Navigate to the scanner folder
cd /path/to/your/scanner/folder

# Make sure you see scanner_main.py when you run:
ls

# Then run:
streamlit run scanner_main.py
```

#### Solution 2: Set Python Path
```bash
# Add current directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Then run:
streamlit run scanner_main.py
```

#### Solution 3: Use Absolute Path
```bash
# Run with full path
streamlit run /full/path/to/scanner_main.py
```

### Verify Directory Structure

Your folder should look like this:
```
your_scanner_folder/
├── scanner_main.py          ← Main file
├── requirements.txt
├── README.md
├── nasdaq100.csv
│
├── modules/                 ← Must exist!
│   ├── __init__.py         ← Must exist!
│   ├── indicators.py
│   ├── patterns.py
│   ├── rule_engine.py
│   └── scanner_engine.py
│
└── pages/                   ← Must exist!
    ├── __init__.py         ← Must exist!
    ├── scanner.py
    ├── charts.py
    ├── configuration.py
    └── workflows.py
```

### Check Files Exist

```bash
# Run this to verify all files are present:
ls -la scanner_main.py
ls -la modules/__init__.py
ls -la modules/indicators.py
ls -la pages/__init__.py
ls -la pages/scanner.py

# All should show file sizes (not errors)
```

### Create Missing __init__.py Files

If `__init__.py` files are missing:
```bash
# Create them:
touch modules/__init__.py
touch pages/__init__.py
```

## ❌ Common Error: No module named 'modules.indicators'

### Fix:
```bash
# Make sure __init__.py exists in modules/
touch modules/__init__.py

# Run from correct directory
cd /path/to/scanner/folder
streamlit run scanner_main.py
```

## ❌ Common Error: No module named 'yfinance'

### Fix:
```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually:
pip install streamlit pandas numpy yfinance plotly ta scipy
```

## ❌ Common Error: ImportError in scanner.py

This means the scanner page can't import the modules.

### Fix:
```bash
# Check that modules directory exists:
ls -la modules/

# Should show:
# __init__.py
# indicators.py
# patterns.py
# rule_engine.py
# scanner_engine.py

# If files are missing, re-download the complete package
```

## ❌ Error: Streamlit not found

### Fix:
```bash
# Install Streamlit
pip install streamlit

# Verify installation
streamlit --version

# Should show: Streamlit, version 1.28.0 or higher
```

## ✅ Complete Setup Verification

Run this checklist:

```bash
# 1. Check Python version (should be 3.8+)
python --version

# 2. Check Streamlit installed
streamlit --version

# 3. Check directory structure
ls scanner_main.py modules/ pages/

# 4. Check __init__.py files exist
ls modules/__init__.py pages/__init__.py

# 5. Check all page files exist
ls pages/scanner.py pages/charts.py pages/configuration.py pages/workflows.py

# 6. Check all module files exist
ls modules/indicators.py modules/patterns.py modules/rule_engine.py modules/scanner_engine.py

# 7. Install dependencies
pip install -r requirements.txt

# 8. Run application
streamlit run scanner_main.py
```

## 🚀 Step-by-Step First Run

```bash
# Step 1: Navigate to folder
cd /path/to/your/scanner/folder

# Step 2: Verify files
ls
# You should see: scanner_main.py, modules/, pages/, requirements.txt

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run application
streamlit run scanner_main.py

# Step 5: Application opens in browser
# If browser doesn't open automatically, go to: http://localhost:8501
```

## 🔍 Debug Mode

If still having issues, run with debug output:

```bash
# Run with verbose output
python -v scanner_main.py

# Or check imports manually:
python -c "import sys; print(sys.path)"
python -c "from pages.scanner import render_scanner_page"
```

## 📁 Re-download if Needed

If files are corrupted or missing:

1. Re-download all files from outputs directory
2. Ensure directory structure is correct
3. Verify all __init__.py files exist
4. Run setup again

## 💡 Quick Test

Test if basic imports work:

```python
# Save as test_imports.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from modules.indicators import IndicatorLibrary
    print("✅ modules.indicators OK")
except Exception as e:
    print(f"❌ modules.indicators ERROR: {e}")

try:
    from pages.scanner import render_scanner_page
    print("✅ pages.scanner OK")
except Exception as e:
    print(f"❌ pages.scanner ERROR: {e}")

print("\nIf all OK, run: streamlit run scanner_main.py")
```

Run it:
```bash
python test_imports.py
```

## 🆘 Still Having Issues?

### Check These:

1. **Python Version**: Must be 3.8 or higher
   ```bash
   python --version
   ```

2. **Virtual Environment**: Are you in the right environment?
   ```bash
   which python
   which pip
   ```

3. **File Permissions**: Can you read the files?
   ```bash
   ls -la scanner_main.py modules/ pages/
   ```

4. **Working Directory**: Are you in the right folder?
   ```bash
   pwd
   ls
   ```

5. **Dependencies**: Are all installed?
   ```bash
   pip list | grep -E "streamlit|pandas|yfinance|plotly|ta|scipy"
   ```

## ✅ Expected Output When Working

When you run `streamlit run scanner_main.py`, you should see:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Then your browser should open automatically to the application.

## 📞 Final Checklist

Before asking for help, verify:

- [ ] Python 3.8+ installed
- [ ] In correct directory (where scanner_main.py is)
- [ ] modules/ directory exists with __init__.py
- [ ] pages/ directory exists with __init__.py
- [ ] All .py files present
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] No typos in folder/file names
- [ ] Not running from inside modules/ or pages/ directory

## 🎉 When It Works

You'll see:
1. Scanner page loads
2. Sidebar shows navigation
3. Can enter symbols
4. Can click buttons
5. No import errors

---

**Still stuck?** Make sure you're running from the folder that contains scanner_main.py (not from inside modules/ or pages/)!

**Working?** Great! Read START_HERE.md for usage guide!
