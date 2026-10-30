# market-data-explorer

Six Python scripts for downloading and analyzing market data.

![dashboard](output/AAPL_dashboard.png)

## Scripts

- `01_sp500_census.py` — S&P 500 constituent data
- `02_leaderboard.py` — market-cap ranking for 10 companies
- `03_golden_cross.py` — AAPL 50/200-day moving-average crossovers
- `04_array_drills.py` — NumPy exercises on prices
- `05_growth_of_10k.py` — returns, CAGR, and volatility
- `06_dashboard.py` — four charts for an entered ticker

Browser version: [Stock Explorer](interactive/README.md).

## Run

```bash
pip install -r requirements.txt
python 06_dashboard.py
```

Run from the repository root. Requires internet access.

## Limitations

Prices and fundamentals come from yfinance and may be incomplete. The S&P 500 constituent list includes current members, not historical membership. Educational project, not investment advice.
