from pathlib import Path

import pandas as pd
import streamlit as st
import yaml

from src.data_loader import load_market_snapshot, read_watchlist
from src.paper_trader import append_paper_events
from src.report_writer import write_csv, write_html
from src.signal_engine import build_signals


ROOT = Path(__file__).resolve().parent
HISTORY_PATH = ROOT / "reports" / "signal_history.csv"
PAPER_LOG_PATH = ROOT / "reports" / "paper_trades.csv"
WATCHLIST_COLUMNS = ["symbol", "name", "tokenized_pair", "category"]
REQUIRED_HISTORY_COLUMNS = {"run_id", "symbol", "timestamp_utc", "final_score", "signal"}

LEGACY_RENAME_MAP = {
    "equity": "symbol",
    "token_pair": "tokenized_pair",
    "equity_price": "reference_price",
    "token_price": "tokenized_price",
    "premium_discount_pct": "premium_discount_percent",
    "spread_pct": "bid_ask_spread_percent",
    "score": "final_score",
    "label": "signal",
    "reason": "notes",
}


def load_config() -> dict:
    config_path = ROOT / "configs" / "config.yaml"
    example_path = ROOT / "configs" / "config.example.yaml"
    selected = config_path if config_path.exists() else example_path
    with selected.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_watchlist(path: Path) -> pd.DataFrame:
    if path.exists():
        watchlist = pd.read_csv(path)
    else:
        watchlist = pd.DataFrame(columns=WATCHLIST_COLUMNS)

    for column in WATCHLIST_COLUMNS:
        if column not in watchlist.columns:
            watchlist[column] = ""

    return watchlist[WATCHLIST_COLUMNS].fillna("")


def save_watchlist(path: Path, watchlist: pd.DataFrame) -> pd.DataFrame:
    cleaned = watchlist.copy()
    for column in WATCHLIST_COLUMNS:
        cleaned[column] = cleaned[column].astype(str).str.strip()

    cleaned = cleaned[cleaned["symbol"] != ""]
    cleaned["symbol"] = cleaned["symbol"].str.upper()
    cleaned = cleaned.drop_duplicates(subset=["symbol"], keep="last")
    cleaned = cleaned.sort_values("symbol")

    path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(path, index=False)
    return cleaned


def normalize_signal_history(history: pd.DataFrame) -> pd.DataFrame:
    if history.empty:
        return history

    normalized = history.rename(columns=LEGACY_RENAME_MAP).copy()

    if "run_id" not in normalized.columns:
        normalized.insert(0, "run_id", "legacy")

    if "signal" not in normalized.columns and "signal_label" in normalized.columns:
        normalized["signal"] = normalized["signal_label"]

    if "final_score" in normalized.columns:
        normalized["final_score"] = pd.to_numeric(normalized["final_score"], errors="coerce")

    if "timestamp_utc" in normalized.columns:
        normalized["timestamp_utc"] = pd.to_datetime(normalized["timestamp_utc"], errors="coerce")

    return normalized


def append_signal_history(signals: pd.DataFrame) -> pd.DataFrame:
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    run_id = pd.Timestamp.utcnow().strftime("%Y%m%d%H%M%S")
    history_rows = signals.copy()
    history_rows.insert(0, "run_id", run_id)

    if HISTORY_PATH.exists():
        existing = normalize_signal_history(pd.read_csv(HISTORY_PATH))
        combined = pd.concat([existing, history_rows], ignore_index=True)
    else:
        combined = history_rows

    if {"run_id", "symbol"}.issubset(combined.columns):
        combined = combined.drop_duplicates(subset=["run_id", "symbol"], keep="last")

    combined.to_csv(HISTORY_PATH, index=False)
    return combined


def load_signal_history() -> pd.DataFrame:
    if HISTORY_PATH.exists():
        return normalize_signal_history(pd.read_csv(HISTORY_PATH))
    return pd.DataFrame()


def run_agent() -> pd.DataFrame:
    config = load_config()
    watchlist_path = ROOT / config["inputs"]["watchlist_path"]

    watchlist = read_watchlist(watchlist_path)
    snapshot = load_market_snapshot(watchlist, config)
    signals = build_signals(snapshot, config)

    write_csv(signals, ROOT / config["outputs"]["latest_signals_csv"])
    write_html(signals, ROOT / config["outputs"]["latest_signals_html"], config)
    append_paper_events(signals, ROOT / config["outputs"]["paper_trades_csv"])
    append_signal_history(signals)

    return signals


def render_landing_section() -> None:
    st.title("Tokenized Securities Research")
    st.subheader("AI intelligence for traditional and tokenized markets.")

    st.markdown(
        """
        Tokenized Securities Research is an open AI research platform exploring how traditional market data,
        tokenized securities, blockchain infrastructure, oracle networks, and alternative data sources can be
        combined into a richer analytical profile for publicly traded securities.

        The project is designed around securities that may trade in two forms: a traditional market reference and
        a tokenized representation. The research objective is to understand whether combining market data,
        tokenized market behavior, on-chain activity, oracle feeds, social intelligence, and AI-generated observations
        can create analytical insight that traditional tools do not currently provide.
        """
    )

    st.markdown("### Intelligence objective")
    st.write(
        "Develop an AI research framework capable of synthesizing multiple independent information sources into a "
        "single intelligence profile for a security that exists in both traditional and tokenized markets."
    )

    badge_col1, badge_col2, badge_col3, badge_col4 = st.columns(4)
    badge_col1.metric("Version", "0.1.1")
    badge_col2.metric("Research Focus", "Security Profiles")
    badge_col3.metric("Data Coverage", "Live + Simulated")
    badge_col4.metric("Stage", "Public Preview")

    st.markdown("### Research inputs")

    col1, col2 = st.columns(2)
    with col1:
        st.write("• Traditional market data")
        st.write("• Tokenized securities data")
        st.write("• Blockchain and on-chain activity")
        st.write("• Oracle network feeds")
    with col2:
        st.write("• Liquidity and spread analysis")
        st.write("• Cross-market pricing behavior")
        st.write("• Social and alternative data")
        st.write("• AI-generated research observations")

    st.info(
        "Version 0.1.1 is a public research preview. Traditional reference prices are live through the current "
        "market data layer. Tokenized market analytics are currently simulated while live blockchain, oracle, "
        "social, and tokenized exchange integrations are developed."
    )

    st.markdown("### Research hypothesis")
    st.write(
        "Securities that exist in both traditional and tokenized markets may reveal analytical relationships that are "
        "not observable through traditional financial analysis alone."
    )


def render_sidebar(watchlist_path: Path) -> bool:
    st.sidebar.header("Research Controls")
    st.sidebar.caption("v0.1.1 public research preview")

    st.sidebar.markdown("**Current Capabilities**")
    st.sidebar.write("• Research universe")
    st.sidebar.write("• Intelligence profile model")
    st.sidebar.write("• Research history")
    st.sidebar.write("• AI research notes")

    st.sidebar.markdown("**Planned Data Sources**")
    st.sidebar.write("• Live traditional market data")
    st.sidebar.write("• Tokenized market data")
    st.sidebar.write("• Blockchain analytics")
    st.sidebar.write("• Oracle networks")
    st.sidebar.write("• Social media intelligence")
    st.sidebar.write("• News intelligence")
    st.sidebar.write("• Wallet analytics")
    st.sidebar.write("• AI-generated research summaries")

    st.sidebar.divider()
    st.sidebar.write("Universe file:")
    st.sidebar.code(str(watchlist_path))
    st.sidebar.write("History file:")
    st.sidebar.code(str(HISTORY_PATH))
    st.sidebar.write("Research notes file:")
    st.sidebar.code(str(PAPER_LOG_PATH))

    st.sidebar.divider()
    return st.sidebar.button("Generate Intelligence Profile")


def render_research_universe(watchlist_path: Path) -> None:
    st.header("Research Universe")
    st.caption("Reference assets and tokenized pairs used to build a security intelligence profile.")

    watchlist = load_watchlist(watchlist_path)

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Reference Assets", len(watchlist))
    metric_col2.metric("Tokenized Pairs", int((watchlist["tokenized_pair"].astype(str).str.strip() != "").sum()))
    metric_col3.metric("Profile Framework", "Prototype")

    edited = st.data_editor(
        watchlist,
        num_rows="dynamic",
        width="stretch",
        key="watchlist_editor",
        column_config={
            "symbol": st.column_config.TextColumn("Reference Symbol", required=True),
            "name": st.column_config.TextColumn("Asset / Security Name"),
            "tokenized_pair": st.column_config.TextColumn("Tokenized Pair"),
            "category": st.column_config.TextColumn("Category"),
        },
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Save Universe"):
            saved = save_watchlist(watchlist_path, edited)
            st.success(f"Research universe saved with {len(saved)} references.")
            st.rerun()

    with col2:
        st.info("Use the blank row at the bottom to add a reference asset or tokenized pair.")


def render_market_signals(signals: pd.DataFrame) -> None:
    st.header("Intelligence Profile")
    st.caption("Current analytical profile generated from available traditional and tokenized research inputs.")

    if signals.empty:
        st.info("No intelligence profile found yet. Click 'Generate Intelligence Profile' to create one.")
        return

    col1, col2, col3, col4 = st.columns(4)
    best_row = signals.sort_values("final_score", ascending=False).iloc[0]
    worst_row = signals.sort_values("final_score", ascending=True).iloc[0]

    col1.metric("Profile Rows", len(signals))
    col2.metric("Highest Score", f"{best_row['symbol']} {best_row['final_score']}")
    col3.metric("Lowest Score", f"{worst_row['symbol']} {worst_row['final_score']}")
    col4.metric("Observation Flags", int(signals["signal"].isin(["STRONG_WATCH", "WATCH"]).sum()))

    st.subheader("Data Coverage")
    coverage_col1, coverage_col2, coverage_col3, coverage_col4 = st.columns(4)
    coverage_col1.metric("Traditional Market", "Live")
    coverage_col2.metric("Tokenized Market", "Simulated")
    coverage_col3.metric("Oracle / On-Chain", "Planned")
    coverage_col4.metric("Social / News", "Planned")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        signal_options = sorted(signals["signal"].dropna().unique())
        selected_signals = st.multiselect("Profile classification", options=signal_options, default=signal_options)

    with filter_col2:
        category_options = sorted(signals["category"].dropna().unique())
        selected_categories = st.multiselect("Category", options=category_options, default=category_options)

    with filter_col3:
        min_score = float(signals["final_score"].min())
        max_score = float(signals["final_score"].max())
        score_range = st.slider("Score range", min_value=-100.0, max_value=100.0, value=(min_score, max_score), step=1.0)

    filtered = signals.copy()

    if selected_signals:
        filtered = filtered[filtered["signal"].isin(selected_signals)]

    if selected_categories:
        filtered = filtered[filtered["category"].isin(selected_categories)]

    filtered = filtered[(filtered["final_score"] >= score_range[0]) & (filtered["final_score"] <= score_range[1])]

    st.subheader("Filtered Intelligence Profile")
    st.dataframe(filtered, width="stretch")

    st.download_button(
        label="Download Intelligence Profile CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="intelligence_profile_filtered.csv",
        mime="text/csv",
    )

    if filtered.empty:
        st.info("No profile rows match the current filters.")
        return

    st.subheader("Profile Detail")
    selected_symbol = st.selectbox("Select a reference asset to review", options=filtered["symbol"].tolist())
    selected_row = filtered[filtered["symbol"] == selected_symbol].iloc[0]

    detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)
    detail_col1.metric("Classification", selected_row["signal"])
    detail_col2.metric("Score", selected_row["final_score"])
    detail_col3.metric("Premium / Discount", f"{selected_row['premium_discount_percent']}%")
    detail_col4.metric("Spread", f"{selected_row['bid_ask_spread_percent']}%")

    st.write(f"**Name:** {selected_row['name']}")
    st.write(f"**Category:** {selected_row['category']}")
    st.write(f"**Tokenized Pair:** {selected_row['tokenized_pair']}")
    st.write(f"**Observation Notes:** {selected_row['notes']}")

    st.subheader("AI Research Observations")
    for _, row in filtered.iterrows():
        st.write(f"**{row['symbol']}**: {row['signal']} with a score of {row['final_score']}. Notes: {row['notes']}.")


def render_signal_history() -> None:
    st.header("Research History")
    history = load_signal_history()

    if history.empty:
        st.info("No research history has been recorded yet. Generate an Intelligence Profile to start building history.")
        return

    missing = REQUIRED_HISTORY_COLUMNS.difference(history.columns)
    if missing:
        st.warning("The existing history file uses an older format and cannot be charted yet.")
        st.caption(f"Missing columns: {', '.join(sorted(missing))}")
        st.dataframe(history, width="stretch")
        return

    history["timestamp_utc"] = pd.to_datetime(history["timestamp_utc"], errors="coerce")
    history = history.dropna(subset=["timestamp_utc", "symbol"])

    if history.empty:
        st.info("Research history exists, but it does not contain usable timestamp and symbol rows yet.")
        return

    history = history.sort_values(["timestamp_utc", "symbol"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Historical Rows", len(history))
    col2.metric("Unique References", history["symbol"].nunique())
    col3.metric("Profiles Captured", history["run_id"].nunique())

    symbols = sorted(history["symbol"].dropna().unique())
    selected_symbols = st.multiselect("Select references for history view", options=symbols, default=symbols)
    filtered = history[history["symbol"].isin(selected_symbols)] if selected_symbols else history

    st.subheader("Score Trend")
    if not filtered.empty:
        chart_data = filtered.pivot_table(index="timestamp_utc", columns="symbol", values="final_score", aggfunc="last").sort_index()
        st.line_chart(chart_data)

    st.subheader("History Table")
    st.dataframe(filtered.sort_values("timestamp_utc", ascending=False), width="stretch")

    st.download_button(
        label="Download Research History",
        data=history.to_csv(index=False).encode("utf-8"),
        file_name="research_history.csv",
        mime="text/csv",
    )


def render_research_journal() -> None:
    st.header("AI Research Notes")
    st.caption("Review research events generated by the intelligence profile model.")

    if not PAPER_LOG_PATH.exists():
        st.info("No AI research notes found yet. Generate an Intelligence Profile to create research events.")
        return

    paper = pd.read_csv(PAPER_LOG_PATH)

    if paper.empty:
        st.info("The AI research notes file exists, but it does not contain any events yet.")
        return

    if "timestamp_utc" in paper.columns:
        paper["timestamp_utc"] = pd.to_datetime(paper["timestamp_utc"], errors="coerce")
        paper = paper.sort_values("timestamp_utc", ascending=False)

    watch_signals = ["WATCH", "STRONG_WATCH"]
    risk_signals = ["CAUTION", "RISK_OFF"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Notes", len(paper))
    col2.metric("Unique References", paper["symbol"].nunique() if "symbol" in paper.columns else "N/A")

    if "signal" in paper.columns:
        col3.metric("Watch Notes", int(paper["signal"].isin(watch_signals).sum()))
        col4.metric("Risk Notes", int(paper["signal"].isin(risk_signals).sum()))
    else:
        col3.metric("Watch Notes", "N/A")
        col4.metric("Risk Notes", "N/A")

    filtered = paper.copy()

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        if "signal" in paper.columns:
            signal_options = sorted(paper["signal"].dropna().unique())
            selected_signals = st.multiselect("Profile classification", options=signal_options, default=signal_options, key="journal_signal_filter")
            if selected_signals:
                filtered = filtered[filtered["signal"].isin(selected_signals)]

    with filter_col2:
        if "symbol" in paper.columns:
            symbol_options = sorted(paper["symbol"].dropna().unique())
            selected_symbols = st.multiselect("Reference", options=symbol_options, default=symbol_options, key="journal_symbol_filter")
            if selected_symbols:
                filtered = filtered[filtered["symbol"].isin(selected_symbols)]

    if filtered.empty:
        st.info("No research notes match the current filters.")
        return

    st.subheader("Most Recent AI Research Notes")
    display_columns = [
        column
        for column in [
            "timestamp_utc",
            "symbol",
            "signal",
            "final_score",
            "reference_price",
            "tokenized_price",
            "premium_discount_percent",
            "bid_ask_spread_percent",
            "notes",
        ]
        if column in filtered.columns
    ]

    st.dataframe(filtered[display_columns] if display_columns else filtered, width="stretch")

    st.download_button(
        label="Download Filtered AI Research Notes",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="ai_research_notes_filtered.csv",
        mime="text/csv",
    )


def main() -> None:
    st.set_page_config(page_title="Tokenized Securities Research", layout="wide")

    config = load_config()
    watchlist_path = ROOT / config["inputs"]["watchlist_path"]

    run_requested = render_sidebar(watchlist_path)
    render_landing_section()

    main_run_col, note_col = st.columns([1, 2])
    with main_run_col:
        run_from_main = st.button("Generate Intelligence Profile", type="primary")
    with note_col:
        st.caption("Generate the current security intelligence profile, then review the output below.")

    if run_requested or run_from_main:
        with st.spinner("Generating intelligence profile..."):
            signals = run_agent()
        st.success("Intelligence profile generated and added to research history.")
    else:
        latest_path = ROOT / config["outputs"]["latest_signals_csv"]
        signals = pd.read_csv(latest_path) if latest_path.exists() else pd.DataFrame()

    universe_tab, profile_tab, history_tab, notes_tab = st.tabs(
        ["Research Universe", "Intelligence Profile", "Research History", "AI Research Notes"]
    )

    with universe_tab:
        render_research_universe(watchlist_path)

    with profile_tab:
        render_market_signals(signals)

    with history_tab:
        render_signal_history()

    with notes_tab:
        render_research_journal()


if __name__ == "__main__":
    main()
