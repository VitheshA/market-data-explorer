import yfinance as yf

aapl = yf.download('AAPL', period='10y')
data = aapl[['Close']]
data.columns = ['Price']
data['SMA50'] = data['Price'].rolling(50).mean()
data['SMA200'] = data['Price'].rolling(200).mean()
data = data.dropna()  # first 199 rows have no 200-day average yet

# A golden cross is the day the answer CHANGES: above today, not above yesterday.
is_above = data['SMA50'] > data['SMA200']
was_below = is_above.shift(1) == False  # day one is NaN, so it can never fake a cross
crossovers = is_above & was_below

data['Price'] = data['Price'].round(2)

for date in data[crossovers].index:
    print(f"{date.strftime('%Y-%m-%d')} was a Golden Cross. Price was ${data.loc[date, 'Price']}.")

print(f"\n{crossovers.sum()} golden crosses in the last 10 years.")
