import os
import subprocess
import sys

# Set the current directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Run Streamlit
subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])