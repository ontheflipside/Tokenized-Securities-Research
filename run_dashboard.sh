#!/usr/bin/env bash
set -e

echo "Starting Tokenized Securities Research..."

if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
else
  echo "Python was not found. Please install Python 3.11 or newer."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creating local Python environment..."
  "$PYTHON_CMD" -m venv .venv
fi

source .venv/bin/activate

echo "Installing required packages..."
python -m pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f "configs/config.yaml" ]; then
  echo "Creating local config file..."
  cp configs/config.example.yaml configs/config.yaml
fi

echo "Launching dashboard..."
streamlit run app.py
