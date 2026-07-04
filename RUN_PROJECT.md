# How to Run Tokenized Securities Research

This guide is for someone who wants to try the project locally without already knowing the full Python and GitHub workflow.

## Option 1: Download the project from GitHub

1. Go to the repository page:

   https://github.com/ontheflipside/Tokenized-Securities-Research

2. Click the green **Code** button.
3. Click **Download ZIP**.
4. Unzip the file.
5. Open the unzipped folder on your computer.

## Option 2: Clone the project with Git

If you already use Git, run:

```bash
git clone https://github.com/ontheflipside/Tokenized-Securities-Research.git
cd Tokenized-Securities-Research
```

## Required software

You need Python installed on your computer.

Recommended version: Python 3.11 or newer.

Check whether Python is installed:

```bash
python --version
```

On some Mac or Linux machines, use:

```bash
python3 --version
```

## Windows quick start

From the project folder, double-click:

```text
run_dashboard_windows.bat
```

Or run this from PowerShell:

```powershell
.\run_dashboard_windows.bat
```

The script will:

1. Create a local Python environment if one does not exist.
2. Install the required packages.
3. Create a local config file if one does not exist.
4. Launch the Streamlit dashboard.

When the dashboard starts, your browser should open automatically.

If it does not open automatically, copy the local URL shown in the terminal. It usually looks like this:

```text
http://localhost:8501
```

## Mac or Linux quick start

From the project folder, run:

```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

The script will create a local environment, install the requirements, create a local config file if needed, and launch the dashboard.

## Manual setup

Use this method if you prefer to run each step yourself.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy configs\config.example.yaml configs\config.yaml
streamlit run app.py
```

### Mac or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp configs/config.example.yaml configs/config.yaml
streamlit run app.py
```

## What to do inside the dashboard

1. Open the **Watchlist** tab.
2. Review or edit the symbols.
3. Click **Run Research Report** in the sidebar.
4. Open **Latest Signals** to review the current research output.
5. Open **Signal History** to review prior runs.
6. Open **Paper Log** to review paper research events.

## Important notes

This is an early research prototype. Tokenized market metrics are currently simulated until a live data provider is connected.

The project does not place trades, connect to brokerage accounts, or execute transactions.
