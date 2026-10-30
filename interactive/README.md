# Stock Explorer

Browser version of P1's four-chart ticker dashboard.

Enter a Yahoo Finance-supported ticker to see moving averages, growth of $10,000 versus SPY, daily returns, and 30-day rolling volatility.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Internet access required for market prices. Calculations can be checked with `python -m pytest -q`.

This is a charting tool, not a backtest. Data comes from yfinance and may be missing. Implementation was AI-assisted.
