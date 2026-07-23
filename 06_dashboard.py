import os

import numpy as np
import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt

tick = input('What ticker do you want: ').upper().strip()

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 9))

# --- Panel 1: price trend, 50-day vs 200-day moving average ---
data = yf.download(tick, period='5y')
data_close = data['Close']
data['sma50'] = data_close.rolling(50).mean()
data['sma200'] = data_close.rolling(200).mean()
data = data.dropna()  # first 199 rows have no 200-day average yet
data.columns = data.columns.droplevel('Ticker')

axes[0, 0].plot(data.index, data['sma50'], label='50-Day SMA', color='b')
axes[0, 0].plot(data.index, data['sma200'], label='200-Day SMA', color='y')
axes[0, 0].set_title(f"{tick}: 50-Day vs 200-Day SMA")
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Share Price (USD)')
axes[0, 0].legend()
axes[0, 0].tick_params(axis='x', rotation=45)

# --- Panel 2: what $10,000 would have become, vs the S&P 500 ---
initial = 10000
ticker_list = [tick, 'SPY']
returns = yf.download(ticker_list, period='5y')
returns = returns['Close'].pct_change()
returns['ticker_invest'] = (1 + returns[tick]).cumprod() * initial
returns['spy_invest'] = (1 + returns['SPY']).cumprod() * initial
returns = returns.dropna()

axes[0, 1].plot(returns.index, returns['ticker_invest'], label=tick, color='r')
axes[0, 1].plot(returns.index, returns['spy_invest'], label='S&P 500 (SPY)', color='k')
axes[0, 1].set_title('Performance of $10,000 Initial Investment')
axes[0, 1].set_xlabel('Date')
axes[0, 1].set_ylabel('Portfolio Value (USD)')
axes[0, 1].legend()
axes[0, 1].tick_params(axis='x', rotation=45)

# --- Panel 3: how often each size of daily move happened ---
axes[1, 0].hist(returns[tick], bins=50, color='steelblue', edgecolor='black')
axes[1, 0].set_title(f"{tick}: Distribution of Daily Returns")
axes[1, 0].set_xlabel('Simple Daily Return')
axes[1, 0].set_ylabel('Frequency')

# --- Panel 4: how bumpy the ride was, 30 days at a time ---
returns['av'] = returns[tick].rolling(30).std() * np.sqrt(252)
returns = returns.dropna()

axes[1, 1].plot(returns.index, returns['av'], color='purple')
axes[1, 1].set_title(f"{tick}: 30-Day Rolling Annualized Volatility")
axes[1, 1].set_xlabel('Date')
axes[1, 1].set_ylabel('Volatility')
axes[1, 1].yaxis.set_major_formatter('{x:.0%}')
axes[1, 1].tick_params(axis='x', rotation=45)

fig.suptitle(f"{tick} Performance & Risk Analysis", fontsize=16, fontweight='bold')
plt.tight_layout()

os.makedirs('output', exist_ok=True)  # so a fresh clone doesn't crash here
fig.savefig(f"output/{tick}_dashboard.png", dpi=150, bbox_inches='tight')
plt.show()
