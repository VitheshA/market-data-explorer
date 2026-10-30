# Stock Explorer (interactive P1 extension)

An optional UI for my existing [P1 Market Data Explorer](https://github.com/VitheshA/market-data-explorer), which already had a command-line ticker input and a four-panel matplotlib figure. This version lets a user enter any **Yahoo Finance-supported ticker** in a browser, then see the same four concepts alongside simple return/risk metrics.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Requires internet access for Yahoo Finance price retrieval. Run `python -m pytest -q` to check mathematical calculations (tests use synthetic data and do not require network access).

## What is and is not claimed

- Four views: price/moving averages, growth of $10,000 vs SPY, return distribution, and rolling annualized volatility.
- Adjusted historical close data, **not** an investable backtest or performance forecast.
- yfinance can return gaps or errors; the program reports missing data instead of inventing values.
- This is a usability extension of P1, **not** third-party validation and not an independent research publication.
- AI-assisted implementation. Verify before presenting as personally authored work.
