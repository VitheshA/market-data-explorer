import pandas as pd
import yfinance as yf

ticker_list = ["NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "META", "AVGO", "TSLA", "JPM", "V"]
tickers_data = {}

# Pull three snapshot fundamentals per ticker
for ticker in ticker_list:
    ticker_info = yf.Ticker(ticker).info
    keys = ['marketCap', 'trailingPE', 'currentPrice']
    tickers_data[ticker] = {k: ticker_info.get(k) for k in keys}  # .get() so a missing field can't crash the loop

# One row per ticker, market cap in billions
data = pd.DataFrame(tickers_data).T
data.index.name = 'Ticker'
data['marketCap'] = (data['marketCap'] / 1_000_000_000).round(2)
data = data.rename(columns={'marketCap': 'Market Cap(B)'})

print('Top 5 by market cap ($B):')
print(data.sort_values('Market Cap(B)', ascending=False).head())

print('\nLowest trailing P/E:')
print(data.sort_values('trailingPE').head(1))
