"""P1 Stock Explorer, interactive Streamlit version.
Run: streamlit run app.py
"""
import re

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import yfinance as yf
from analytics import align_growth, summary_metrics, rolling_annual_volatility, validate_close

st.set_page_config(page_title="Stock Explorer | Quant Projects", layout="wide")
st.title("Stock Explorer")
st.caption("Built from P1: any Yahoo Finance-supported ticker vs SPY. Educational analysis, not investment advice.")

symbol = st.text_input("Ticker symbol", value="AAPL").upper().strip()
period = st.selectbox("History", ["1y", "3y", "5y", "10y"], index=2)

if not re.fullmatch(r"[A-Z0-9^._=-]{1,15}", symbol):
    st.error("Enter a valid ticker symbol, such as AAPL, NVDA, or MSFT.")
    st.stop()

@st.cache_data(ttl=60 * 60, show_spinner=False)
def load_close(ticker: str, history: str) -> pd.Series:
    df = yf.download(ticker, period=history, auto_adjust=True, progress=False, threads=False)
    if df.empty or "Close" not in df:
        raise ValueError(f"No price history available for {ticker}")
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return validate_close(close.rename(ticker), ticker)

try:
    close = load_close(symbol, period)
    spy = load_close("SPY", period)
    growth = align_growth(close, spy)
    m = summary_metrics(close.loc[growth.index])
except Exception as exc:
    st.error(f"Unable to chart {symbol}: {exc}. Check the symbol and internet access.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total return", f"{m['total_return']:.1%}")
c2.metric("CAGR", f"{m['cagr']:.1%}")
c3.metric("Annualized volatility", f"{m['annual_volatility']:.1%}")
c4.metric("Maximum drawdown", f"{m['max_drawdown']:.1%}")

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
ma50 = close.rolling(50).mean()
ma200 = close.rolling(200).mean()
axes[0, 0].plot(close.index, close, label="Adjusted close", linewidth=1)
axes[0, 0].plot(ma50.index, ma50, label="50-day average", linewidth=1)
axes[0, 0].plot(ma200.index, ma200, label="200-day average", linewidth=1)
axes[0, 0].set_title(f"{symbol}: price and moving averages")
axes[0, 0].legend(fontsize=8)
axes[0, 1].plot(growth.index, growth["Stock"], label=symbol)
axes[0, 1].plot(growth.index, growth["SPY"], label="SPY")
axes[0, 1].set_title("Growth of $10,000 (first shared trading day)")
axes[0, 1].legend()
returns = close.pct_change().dropna()
axes[1, 0].hist(returns, bins=40)
axes[1, 0].set_title("Daily return distribution")
axes[1, 0].set_xlabel("Daily simple return")
vol = rolling_annual_volatility(close)
axes[1, 1].plot(vol.index, vol)
axes[1, 1].set_title("30-day rolling annualized volatility")
axes[1, 1].set_ylabel("Volatility")
for ax in axes.flat:
    ax.grid(alpha=0.15)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)
st.caption("Adjusted Yahoo Finance data may be incomplete or revised. SPY approximates the S&P 500, not the full total-return index. No forecast or trading recommendation is implied.")

with st.expander("What the charts mean"):
    st.markdown("""**Moving averages:** smoothed past prices, not predictive guarantees.  
**Growth of $10,000:** a hindsight comparison normalized to the same starting date.  
**Return distribution:** how often different daily moves occurred.  
**Rolling volatility:** how variable the recent returns have been (annualized by √252).""")
