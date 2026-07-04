@echo off
setlocal

echo Starting Tokenized Securities Research...

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Please install Python 3.11 or newer from https://www.python.org/downloads/
    pause
    exit /b 1
)

if not exist .venv (
    echo Creating local Python environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing required packages...
python -m pip install --upgrade pip
pip install -r requirements.txt

if not exist configs\config.yaml (
    echo Creating local config file...
    copy configs\config.example.yaml configs\config.yaml >nul
)

echo Launching dashboard...
streamlit run app.py

pause
