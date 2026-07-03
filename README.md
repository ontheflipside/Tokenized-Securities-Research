# Tokenized Equity Strategy Agent

An early stage research dashboard and signal engine for studying tokenized equity market behavior.

This project is designed to compare tokenized equity instruments against their underlying public equity references, generate structured watch signals, and preserve paper trading events for later analysis. It is intentionally built as a research and alerting workflow first. It does not place trades, execute orders, or provide investment advice.

## Current status

Prototype / version 0.1.0.

The current implementation includes a local signal engine, configurable watchlist, generated CSV and HTML reports, paper event logging, and a Streamlit dashboard. Tokenized market metrics are currently simulated until a reliable live tokenized market data source is connected.

## Why this matters

Tokenized equities may trade on different market rails than traditional listed equities. They can have different liquidity, spreads, trading hours, price dislocations, and execution risks. The purpose of this project is to study those differences in a repeatable way before any live execution logic is considered.

The research thesis is simple: if tokenized equity markets develop real liquidity, useful signals may come from market structure, premium or discount behavior, liquidity depth, and price dislocation rather than ordinary stock picking.

## What it does

The agent monitors a configurable watchlist of tokenized equity pairs, such as `AAPLx/USD`, `TSLAx/USD`, and `NVDAx/USD`, compares them against reference equity data, and produces a signal report.

The signal engine currently focuses on:

1. Tokenized equity premium or discount versus the underlying stock.
2. Order book imbalance on the tokenized market.
3. Liquidity depth and estimated slippage.
4. Risk controls, including maximum position size, spread limits, and stop thresholds.
5. Paper signal logging for future performance review.

## What it does not do

This project does not:

- Execute live trades.
- Connect to a brokerage account.
- Connect to a crypto exchange account.
- Provide investment, legal, tax, or financial advice.
- Guarantee signal quality or trading performance.

## Repository structure

```text
.
├── app.py                         # Streamlit dashboard
├── configs/
│   └── config.example.yaml         # Safe example configuration
├── data/
│   └── watchlist.csv               # Research watchlist
├── reports/
│   └── .gitkeep                    # Generated reports are ignored
├── scripts/
│   └── run_agent.py                # Command line signal runner
├── src/
│   ├── data_loader.py              # Market and watchlist loading
│   ├── paper_trader.py             # Paper event logging
│   ├── report_writer.py            # CSV and HTML output
│   └── signal_engine.py            # Signal scoring logic
├── requirements.txt
└── README.md
```

## Setup

Create a virtual environment and install the requirements.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp configs/config.example.yaml configs/config.yaml
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy configs\config.example.yaml configs\config.yaml
```

## Run from the command line

```bash
python scripts/run_agent.py
```

## Run the dashboard

```bash
streamlit run app.py
```

## Outputs

The agent creates local report files under `reports/`:

```text
reports/latest_signals.csv
reports/latest_signals.html
reports/paper_trades.csv
reports/signal_history.csv
```

Generated report files are intentionally ignored by Git so local research output is not accidentally published.

## Signal interpretation

The final score ranges from negative to positive.

```text
score >= 70     strong watch signal
score 40 to 69  positive watch signal
score -39 to 39 neutral
score -40 to -69 caution or possible exit
score <= -70    strong risk-off watch signal
```

These labels are research classifications only. They are not trading recommendations.

## Configuration

The default example configuration is stored at `configs/config.example.yaml`. Copy it to `configs/config.yaml` for local use.

The local `configs/config.yaml` file is ignored by Git because future versions may include provider credentials or user-specific overrides.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the development plan.

Near-term priorities include:

- Connect a real tokenized market data provider.
- Improve premium and discount calculations.
- Add historical backtesting.
- Add signal performance tracking.
- Add contribution-ready issues for data, dashboard, scoring, and documentation.

## Contributing

This is an early public prototype. Contributions are welcome, especially around data source integration, market structure research, signal scoring, backtesting, dashboard design, and documentation.

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).

## Disclaimer

This software is provided for research and educational purposes only. It is not investment advice, financial advice, or a recommendation to buy, sell, hold, or short any security, token, derivative, or financial instrument. Use at your own risk.
