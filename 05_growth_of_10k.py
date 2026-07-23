import numpy as np
import pandas as pd
import yfinance as yf

tickers = ['AAPL', 'MSFT', 'AMZN', 'SPY']
years = 5
initial = 10000

data = yf.download(tickers, period=f'{years}y')
data = data['Close']

# Daily returns, then the running value of a $10,000 investment
for ticker in tickers:
    data[f"{ticker}_Return"] = data[ticker].pct_change()
data = data.iloc[1:]  # drop the first row, which has no return

for ticker in tickers:
    data[f"{ticker} value"] = (1 + data[f"{ticker}_Return"]).cumprod() * initial

# One summary row per ticker: where it ended, how fast it compounded, how rough the ride was
ticker_summary = []
for ticker in tickers:
    ticker_price = data[f"{ticker} value"].iloc[-1]
    CAGR = (ticker_price / initial) ** (1 / years) - 1
    AV = data[f"{ticker}_Return"].std() * np.sqrt(252)
    ticker_summary.append({
        'Ticker': ticker,
        'Final Value': ticker_price.round(2),
        'CAGR': f"{CAGR:.2%}",
        'Annualized Volatility': f"{AV:.2%}",
    })

summary_df = pd.DataFrame(ticker_summary)
print(summary_df.to_string(index=False))
