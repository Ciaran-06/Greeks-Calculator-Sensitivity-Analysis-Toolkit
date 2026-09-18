import yfinance as yf
import pandas as pd

spy = yf.Ticker("SPY")


expirations = spy.options

all_calls = []

for exp_date in expirations:
    chain = spy.option_chain(date=exp_date)
    calls = chain.calls.copy()
    calls['expiry'] = exp_date
    all_calls.append(calls)
    print(f"Loaded {exp_date}: {len(calls)} contracts")


df = pd.concat(all_calls, ignore_index=True)

spot_price = spy.history(period='1d')['Close'].iloc[-1]
df['underlying_last'] = spot_price
df['quote_date'] = pd.Timestamp.today()

print(f"\nTotal records: {len(df)}")
print(f"Spot price: {spot_price}")
print(df.head())

df.to_csv('./data/cleaned/spy_options_all_expiries.csv', index=False)
print("\nSaved to spy_options_all_expiries.csv")