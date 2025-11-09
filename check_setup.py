#!/usr/bin/env python3
"""
Setup Verification Script
Checks that all files are in place before running the scanner
"""

import os
import sys

def check_file(path, description):
    """Check if a file exists"""
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"✅ {description}: {path} ({size} bytes)")
        return True
    else:
        print(f"❌ MISSING: {description}: {path}")
        return False

def check_directory(path, description):
    """Check if a directory exists"""
    if os.path.isdir(path):
        files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        print(f"✅ {description}: {path} ({files} files)")
        return True
    else:
        print(f"❌ MISSING: {description}: {path}")
        return False

def main():
    print("=" * 60)
    print("  Advanced Market Scanner - Setup Verification")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check main files
    print("📄 Checking Main Files:")
    print("-" * 60)
    all_good &= check_file("scanner_main.py", "Main application")
    all_good &= check_file("requirements.txt", "Dependencies file")
    all_good &= check_file("README.md", "Documentation")
    all_good &= check_file("nasdaq100.csv", "Sample watchlist")
    print()
    
    # Check directories
    print("📁 Checking Directories:")
    print("-" * 60)
    all_good &= check_directory("modules", "Core modules directory")
    all_good &= check_directory("pages", "Pages directory")
    print()
    
    # Check module files
    print("🔧 Checking Module Files:")
    print("-" * 60)
    all_good &= check_file("modules/__init__.py", "Modules package init")
    all_good &= check_file("modules/indicators.py", "Indicators module")
    all_good &= check_file("modules/patterns.py", "Patterns module")
    all_good &= check_file("modules/rule_engine.py", "Rule engine module")
    all_good &= check_file("modules/scanner_engine.py", "Scanner engine module")
    print()
    
    # Check page files
    print("📱 Checking Page Files:")
    print("-" * 60)
    all_good &= check_file("pages/__init__.py", "Pages package init")
    all_good &= check_file("pages/scanner.py", "Scanner page")
    all_good &= check_file("pages/charts.py", "Charts page")
    all_good &= check_file("pages/configuration.py", "Configuration page")
    all_good &= check_file("pages/workflows.py", "Workflows page")
    print()
    
    # Check Python version
    print("🐍 Checking Python Version:")
    print("-" * 60)
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        all_good = False
    print()
    
    # Check imports
    print("📦 Checking Imports:")
    print("-" * 60)
    
    packages = {
        'streamlit': 'Streamlit framework',
        'pandas': 'Data manipulation',
        'numpy': 'Numerical computing',
        'yfinance': 'Yahoo Finance data',
        'plotly': 'Interactive charts',
        'ta': 'Technical analysis',
        'scipy': 'Scientific computing'
    }
    
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"✅ {package:15} - {description}")
        except ImportError:
            print(f"❌ {package:15} - NOT INSTALLED")
            all_good = False
    print()
    
    # Check custom imports
    print("🔗 Checking Custom Imports:")
    print("-" * 60)
    
    # Add current directory to path
    sys.path.insert(0, os.getcwd())
    
    try:
        from modules.indicators import IndicatorLibrary
        print("✅ modules.indicators - OK")
    except Exception as e:
        print(f"❌ modules.indicators - ERROR: {e}")
        all_good = False
    
    try:
        from modules.patterns import ChartPatterns
        print("✅ modules.patterns - OK")
    except Exception as e:
        print(f"❌ modules.patterns - ERROR: {e}")
        all_good = False
    
    try:
        from modules.rule_engine import RuleEngine
        print("✅ modules.rule_engine - OK")
    except Exception as e:
        print(f"❌ modules.rule_engine - ERROR: {e}")
        all_good = False
    
    try:
        from modules.scanner_engine import ScannerEngine
        print("✅ modules.scanner_engine - OK")
    except Exception as e:
        print(f"❌ modules.scanner_engine - ERROR: {e}")
        all_good = False
    
    try:
        from pages.scanner import render_scanner_page
        print("✅ pages.scanner - OK")
    except Exception as e:
        print(f"❌ pages.scanner - ERROR: {e}")
        all_good = False
    
    try:
        from pages.charts import render_charts_page
        print("✅ pages.charts - OK")
    except Exception as e:
        print(f"❌ pages.charts - ERROR: {e}")
        all_good = False
    
    print()
    
    # Final verdict
    print("=" * 60)
    if all_good:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("You're ready to run the scanner:")
        print("  streamlit run scanner_main.py")
    else:
        print("❌ SOME CHECKS FAILED!")
        print()
        print("Fix the issues above, then run:")
        print("  python check_setup.py")
    print("=" * 60)
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
