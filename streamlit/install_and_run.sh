#!/bin/bash

echo "SmartRunning - Streamlit Frontend Setup"
echo "======================================="

# Check for pip
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed or not in PATH."
    echo "Please install pip first: https://pip.pypa.io/en/stable/installation/"
    exit 1
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in PATH."
    echo "Please install Python first: https://www.python.org/downloads/"
    exit 1
fi

echo "Installing core dependencies..."
pip install streamlit

echo "Running the app (with limited functionality)..."
echo "For full functionality, run: pip install -r requirements.txt"
streamlit run app.py

# The app will handle missing dependencies gracefully