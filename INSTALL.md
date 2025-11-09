# 📦 Installation Guide - Advanced Market Scanner

## ⚡ Quick Install (3 Steps)

### Step 1: Extract the ZIP file
```bash
# Extract to your desired location
unzip AdvancedMarketScanner.zip
cd AdvancedMarketScanner
```

### Step 2: Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
# Run the scanner
streamlit run scanner_main.py
```

That's it! The application will open at `http://localhost:8501`

---

## 📋 Prerequisites

### Required:
- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (comes with Python)
- **Internet connection** - For downloading market data

### Check Your Python Version:
```bash
python --version
# or
python3 --version

# Should show: Python 3.8.x or higher
```

---

## 🚀 Detailed Installation

### Option 1: Quick Install Script (Recommended)

**For Mac/Linux:**
```bash
cd AdvancedMarketScanner
chmod +x RUN_ME.sh
./RUN_ME.sh
```

**For Windows:**
```cmd
cd AdvancedMarketScanner
python -m pip install -r requirements.txt
streamlit run scanner_main.py
```

### Option 2: Manual Installation

#### 1. Extract Files
```bash
unzip AdvancedMarketScanner.zip
cd AdvancedMarketScanner
```

#### 2. (Optional) Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Verify Installation
```bash
python check_setup.py
```

This will verify:
- ✅ All files present
- ✅ Python version correct
- ✅ Dependencies installed
- ✅ Imports working

#### 5. Run Application
```bash
streamlit run scanner_main.py
```

---

## 📁 Directory Structure

After extraction, you should see:

```
AdvancedMarketScanner/
├── scanner_main.py          ← Main application
├── requirements.txt         ← Python dependencies
├── check_setup.py           ← Setup verification
├── RUN_ME.sh                ← Quick start script
├── README.md                ← Documentation
├── INSTALL.md               ← This file
│
├── data/                    ← Sample data
│   └── nasdaq100.csv        ← 96 stock symbols
│
├── docs/                    ← Documentation
│   ├── START_HERE.md        ← Quick start
│   ├── QUICK_FIX.md         ← Troubleshooting
│   ├── TROUBLESHOOTING.md   ← Detailed help
│   ├── INDEX.md             ← Doc index
│   └── ...
│
├── modules/                 ← Core functionality
│   ├── __init__.py
│   ├── indicators.py        ← 13+ indicators
│   ├── patterns.py          ← 11+ patterns
│   ├── rule_engine.py       ← Rule logic
│   └── scanner_engine.py    ← Scanner engine
│
└── pages/                   ← User interface
    ├── __init__.py
    ├── scanner.py           ← Scanner page
    ├── charts.py            ← Charts page
    ├── configuration.py     ← Settings
    └── workflows.py         ← Workflows
```

---

## 🔧 Dependencies

The following packages will be installed:

```
streamlit==1.28.0      # Web application framework
pandas==2.1.1          # Data manipulation
numpy==1.25.2          # Numerical computing
yfinance==0.2.28       # Yahoo Finance data
plotly==5.17.0         # Interactive charts
ta==0.11.0             # Technical analysis
scipy==1.11.3          # Scientific computing
```

---

## ✅ Verify Installation

Run the setup checker:

```bash
python check_setup.py
```

Expected output:
```
============================================================
  Advanced Market Scanner - Setup Verification
============================================================

📄 Checking Main Files:
------------------------------------------------------------
✅ Main application: scanner_main.py (XXXX bytes)
✅ Dependencies file: requirements.txt (XXX bytes)
✅ Documentation: README.md (XXXX bytes)
✅ Sample watchlist: data/nasdaq100.csv (XXX bytes)

📁 Checking Directories:
------------------------------------------------------------
✅ Core modules directory: modules (5 files)
✅ Pages directory: pages (5 files)

... (more checks)

============================================================
✅ ALL CHECKS PASSED!

You're ready to run the scanner:
  streamlit run scanner_main.py
============================================================
```

---

## 🎯 First Run

After installation:

1. **Open Terminal/Command Prompt**
   ```bash
   cd /path/to/AdvancedMarketScanner
   ```

2. **Run Application**
   ```bash
   streamlit run scanner_main.py
   ```

3. **Browser Opens Automatically**
   - If not, go to: `http://localhost:8501`

4. **Load Symbols**
   - Upload: `data/nasdaq100.csv`
   - Or enter manually: `AAPL,MSFT,GOOGL`

5. **Run Scan**
   - Click "🚀 Run Scan"
   - View results!

---

## 🐛 Troubleshooting

### Problem: Python not found
```bash
# Install Python from: https://www.python.org/downloads/
# Then verify:
python --version
```

### Problem: pip not found
```bash
# Install pip:
python -m ensurepip --upgrade
```

### Problem: Permission denied
```bash
# On Mac/Linux:
chmod +x RUN_ME.sh
chmod +x check_setup.py
```

### Problem: Module not found errors
```bash
# Reinstall dependencies:
pip install -r requirements.txt --upgrade

# Or install individually:
pip install streamlit pandas numpy yfinance plotly ta scipy
```

### Problem: Can't run check_setup.py
```bash
# Make sure you're in the right directory:
cd AdvancedMarketScanner
ls scanner_main.py  # Should show the file

# Run with python:
python check_setup.py
```

### Problem: Port 8501 already in use
```bash
# Kill existing Streamlit:
pkill -f streamlit

# Or use different port:
streamlit run scanner_main.py --server.port 8502
```

### Problem: Import errors when running
```bash
# Make sure you're running from AdvancedMarketScanner directory:
pwd  # Should end with /AdvancedMarketScanner
cd /path/to/AdvancedMarketScanner
streamlit run scanner_main.py
```

See **docs/TROUBLESHOOTING.md** for more solutions.

---

## 🌐 Network & Firewall

The application:
- Runs locally on `http://localhost:8501`
- Downloads market data from Yahoo Finance (requires internet)
- No external data sharing
- No authentication required

**Firewall:**
- Allow Python/Streamlit through firewall if prompted
- Allow outbound connections to Yahoo Finance

---

## 🔄 Updating

To update the application:

1. **Backup your workflows** (if you created custom ones)
2. **Extract new version** to a different folder
3. **Copy your workflows** (if needed)
4. **Reinstall dependencies:**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

---

## 🗑️ Uninstalling

To remove the application:

1. **Delete the folder:**
   ```bash
   rm -rf /path/to/AdvancedMarketScanner
   ```

2. **Remove virtual environment** (if you created one):
   ```bash
   rm -rf venv
   ```

3. **(Optional) Uninstall packages:**
   ```bash
   pip uninstall streamlit pandas numpy yfinance plotly ta scipy
   ```

---

## 📱 Platform-Specific Notes

### Windows
- Use Command Prompt or PowerShell
- Use `python` instead of `python3`
- Use `\` for paths instead of `/`
- Example: `cd C:\Users\YourName\AdvancedMarketScanner`

### Mac/Linux
- Use Terminal
- May need `python3` and `pip3`
- May need `sudo` for system-wide installation
- Example: `cd ~/AdvancedMarketScanner`

### Docker (Advanced)
```dockerfile
# Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "scanner_main.py"]
```

```bash
# Build and run
docker build -t market-scanner .
docker run -p 8501:8501 market-scanner
```

---

## 🎓 Next Steps

After installation:

1. **Read Quick Start**: `docs/START_HERE.md`
2. **Try First Scan**: Upload `data/nasdaq100.csv`
3. **Explore Features**: Charts, Workflows, Configuration
4. **Read Documentation**: `README.md`

---

## 📞 Getting Help

### Documentation Files:
- **START_HERE.md** - Quick start (3 minutes)
- **QUICK_FIX.md** - Common issues (1 minute)
- **TROUBLESHOOTING.md** - Detailed help (10 minutes)
- **README.md** - Complete guide (20 minutes)

### Verify Installation:
```bash
python check_setup.py
```

### Test Imports:
```bash
python -c "from pages.scanner import render_scanner_page; print('OK')"
```

---

## ✅ Installation Checklist

Before running, verify:

- [ ] Python 3.8+ installed
- [ ] Extracted ZIP file
- [ ] In AdvancedMarketScanner directory
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Ran setup checker (`python check_setup.py`)
- [ ] All checks passed

---

## 🚀 Ready!

You're all set! Run:

```bash
streamlit run scanner_main.py
```

The application opens at **http://localhost:8501**

Happy trading! 📈

---

**Version**: 2.0 - Complete Implementation  
**Release**: November 2025  
**Support**: Full documentation included

---

*For troubleshooting, see docs/TROUBLESHOOTING.md*  
*For quick start, see docs/START_HERE.md*
