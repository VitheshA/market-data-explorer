import numpy as np
import yfinance as yf

# Pull 10 years of closes and pull the column out as a plain NumPy array
aapl = yf.download('AAPL', period='10y', auto_adjust=True)
closes = aapl[['Close']].to_numpy().flatten()

# Boolean mask: a comparison returns True/False per day, and True counts as 1
print(f"There were {(closes > 200).sum()} days with a close above $200.")

print(f"${closes.max().round(2)} was the highest close.")

# Negative slicing counts back from the end
print(f"The last five closes are {closes[-5:].round(2)}")
