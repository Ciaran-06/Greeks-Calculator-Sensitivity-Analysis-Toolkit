import yfinance as yf
import pandas as pd
import sys

if len(sys.argv) < 2:
    print("Usage: python data_ingestion.py <ticker>")
    sys.exit(1)

ticker_symbol = sys.argv[1].upper()
ticker = yf.Ticker(ticker_symbol)

print(f"Fetching {ticker_symbol} options data...")

expirations = ticker.options

all_calls = []

for exp_date in expirations:
    chain = ticker.option_chain(date=exp_date)
    calls = chain.calls.copy()
    calls['expiry'] = exp_date
    all_calls.append(calls)
    print(f"Loaded {exp_date}: {len(calls)} contracts")

df = pd.concat(all_calls, ignore_index=True)

spot_price = ticker.history(period='1d')['Close'].iloc[-1] 
df['underlying_last'] = spot_price
df['quote_date'] = pd.Timestamp.today()

print(f"\nTotal records: {len(df)}")
print(f"Spot price: {spot_price}")
print(df.head())

df.to_csv(f'./data/uncleaned/{ticker_symbol.upper()}.csv', index=False)
print(f"\nSaved uncleaned data to {ticker_symbol}.csv")

print(df.columns)

#for greeks we need rn we have
#Index(['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask',
#       'change', 'percentChange', 'volume', 'openInterest',
#       'impliedVolatility', 'inTheMoney', 'contractSize', 'currency', 'expiry',
#       'underlying_last', 'quote_date'],
#      dtype='object')
# we need spot, strike, experation, vol, risk-free-rate

columns_needed = ['lastPrice', 'strike', 'expiry', 'impliedVolatility', 'underlying_last']
cleaneded_df = df[columns_needed]

cleaneded_df.to_csv(f'./data/cleaned/{ticker_symbol.upper()}.csv', index=False)