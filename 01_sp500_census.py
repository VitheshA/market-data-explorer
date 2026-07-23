import os

import pandas as pd

sp500 = pd.read_csv('data/sp500_constituents.csv')

# How many companies are in each GICS sector?
sp500sec = sp500.groupby('GICS Sector').count().sort_values('Symbol', ascending=False)['Symbol']

# Which sector has the most companies headquartered in California?
sp500['Location'] = sp500['Headquarters Location'].str.split(',').str[-1].str.strip()
sp500loc = sp500.groupby('Location').get_group('California').groupby('GICS Sector').count().sort_values('Symbol', ascending=False)['Symbol']

# Every company added to the index since 2024
sp500['Year'] = sp500['Date added'].str.split('-').str[0].astype(int)
sp500late = sp500[sp500['Year'] >= 2024][['Symbol', 'Date added']].sort_values('Date added')

# The 5 companies that have been in the index the longest
sp500early = sp500.sort_values('Date added')[['Symbol', 'Date added']].head()

print('Companies per GICS sector:')
print(sp500sec)

print('\nCalifornia-headquartered companies, by sector:')
print(sp500loc)

print(f"\nAdded to the index since 2024 ({len(sp500late)} companies):")
print(sp500late.to_string(index=False))

print('\nLongest-standing members:')
print(sp500early.to_string(index=False))

# Save the cleaned table (with the Location and Year columns added)
os.makedirs('output', exist_ok=True)
sp500.to_csv('output/sp500_census.csv', index=False)
print('\nSaved output/sp500_census.csv')
