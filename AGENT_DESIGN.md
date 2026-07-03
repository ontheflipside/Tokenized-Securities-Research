# Research Platform Design

## Objective

Build a practical tokenized securities research platform that can identify pricing, liquidity, and demand dislocations between tokenized instruments and their reference assets.

## Version one strategy

The first version is an alerting and research platform. It does not trade live. It scores market conditions and creates a paper research log.

## Core signals

### 1. Premium or discount

```text
(tokenized price - reference asset price) / reference asset price
```

This identifies whether the tokenized version is trading rich or cheap compared with its reference asset.

### 2. Order book imbalance

```text
(bid depth - ask depth) / (bid depth + ask depth)
```

Positive imbalance means buyers are providing more depth than sellers near the current price. Negative imbalance means the opposite.

### 3. Liquidity depth

Measures how much dollar value sits within 1 percent of the midpoint price.

### 4. Spread

Measures the cost of entering and exiting a position in the tokenized market.

## Development path

Phase one is an internal research system. Phase two is a public research dashboard. Phase three is a data and signal quality framework. Phase four is a broader market structure research platform only after a documented performance and data integrity record exists.

## Future modules

1. On-chain wallet flow tracking.
2. Tokenized security issuance, mint, and burn monitoring where available.
3. Reddit and X sentiment scoring.
4. Macro volatility filter.
5. Earnings calendar awareness.
6. Sector rotation model.
7. Automated alerting through email or Teams.
8. Streamlit dashboard.
9. Backtesting engine.
10. Human-reviewed research workflow.
