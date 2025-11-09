#!/bin/bash
echo "========================================"
echo "  Advanced Market Scanner"
echo "  Starting Application..."
echo "========================================"
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt --break-system-packages 2>/dev/null || pip install -r requirements.txt
echo ""
echo "Launching Streamlit application..."
echo "The app will open in your browser at http://localhost:8501"
echo ""
streamlit run scanner_main.py
