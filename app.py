from pathlib import Path

import pandas as pd
import streamlit as st
import yaml

from src.data_loader import load_market_snapshot, read_watchlist
from src.signal_engine import build_signals
from src.report_writer import write_csv, write_html
from src.paper_trader import append_paper_events


ROOT = Path(__file__).resolve().parent


def load_config() -> dict:
    config_path = ROOT / "configs" / "config.yaml"
    example_path = ROOT / "configs" / "config.example.yaml"
    selected = config_path if config_path.exists() else example_path

    with selected.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def run_agent() -> pd.DataFrame:
    config = load_config()
    watchlist_path = ROOT / config["inputs"]["watchlist_path"]

    watchlist = read_watchlist(watchlist_path)
    snapshot = load_market_snapshot(watchlist, config)
    signals = build_signals(snapshot, config)

    write_csv(signals, ROOT / config["outputs"]["latest_signals_csv"])
    write_html(signals, ROOT / config["outputs"]["latest_signals_html"], config)
    append_paper_events(signals, ROOT / config["outputs"]["paper_trades_csv"])

    return signals


def main() -> None:
    st.set_page_config(
        page_title="Tokenized Equity Strategy Agent",
        layout="wide",
    )

    st.title("Tokenized Equity Strategy Agent")
    st.caption("Research dashboard for tokenized equity signal analysis.")

    st.warning(
        "This is a research tool. It does not place trades or execute orders. "
        "Current tokenized market metrics are placeholders until a live data provider is connected."
    )

    config = load_config()
    watchlist_path = ROOT / config["inputs"]["watchlist_path"]

    st.sidebar.header("Project Controls")
    st.sidebar.write("Watchlist file:")
    st.sidebar.code(str(watchlist_path))

    if st.sidebar.button("Run Signal Report"):
        with st.spinner("Running signal engine..."):
            signals = run_agent()
        st.success("Signal report generated.")
    else:
        latest_path = ROOT / config["outputs"]["latest_signals_csv"]
        if latest_path.exists():
            signals = pd.read_csv(latest_path)
        else:
            signals = pd.DataFrame()

    st.header("Watchlist")

    if watchlist_path.exists():
        watchlist = pd.read_csv(watchlist_path)
        st.dataframe(watchlist, use_container_width=True)
    else:
        st.error("Watchlist file not found.")

    st.header("Latest Signals")

    if signals.empty:
        st.info("No signal report found yet. Click 'Run Signal Report' in the sidebar.")
        return

    col1, col2, col3, col4 = st.columns(4)

    best_row = signals.sort_values("final_score", ascending=False).iloc[0]
    worst_row = signals.sort_values("final_score", ascending=True).iloc[0]

    col1.metric("Signals Generated", len(signals))
    col2.metric("Best Score", f"{best_row['symbol']} {best_row['final_score']}")
    col3.metric("Weakest Score", f"{worst_row['symbol']} {worst_row['final_score']}")
    col4.metric("Watch Signals", int(signals["signal"].isin(["STRONG_WATCH", "WATCH"]).sum()))

    st.dataframe(signals, use_container_width=True)

    csv_data = signals.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV Report",
        data=csv_data,
        file_name="latest_signals.csv",
        mime="text/csv",
    )

    st.subheader("Plain English Summary")

    for _, row in signals.iterrows():
        st.write(
            f"**{row['symbol']}**: {row['signal']} with a score of "
            f"{row['final_score']}. Notes: {row['notes']}."
        )


if __name__ == "__main__":
    main()
