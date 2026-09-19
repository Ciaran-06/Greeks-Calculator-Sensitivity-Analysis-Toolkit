import yfinance as yf
import pandas as pd
import sys

if len(sys.argv) < 2:
    print("Usage: python data_ingestion.py <ticker>")
    sys.exit(1)

ticker_symbol = sys.argv[1].upper()
ticker = yf.Ticker(ticker_symbol)

#risk free rate
irx = yf.Ticker("^IRX")
r = irx.history(period="5d")['Close'].iloc[-1] / 100

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
old_df_len = len(df)

ticker_history = ticker.history(period='5d')
last_day = ticker_history.index[-1].tz_localize(None)

df['underlying_last'] = ticker_history['Close'].iloc[-1]
df['r'] = r
df['quote_date'] = last_day

df['mid_price'] = (df['bid'] + df['ask']) / 2

df = df[df['bid'] > 0]
bid_filter = len(df)
print(f"{old_df_len - bid_filter} row diffrence from bid filter")

df = df[df['impliedVolatility'] > 0.01]
iv_filter = len(df)
print(f'{bid_filter - iv_filter} row diffrence from iv filter')

df['T'] = (pd.to_datetime(df['expiry']) - df['quote_date'].dt.normalize()).dt.days / 365
df = df[df['T'] >= (7/365)]
exp_filter = len(df)
print(f'{iv_filter - exp_filter} row diffrence from experation filter')

df = df[(df['strike']/df['underlying_last']).between(0.8,1.2)]
far_filter = len(df)
print(f'{exp_filter - far_filter} row diffrence from far from money filter')

print(f'{old_df_len - len(df)} total row diffrence ')
print(f"\nTotal records: {len(df)}")
print(f"Spot price: {ticker_history['Close'].iloc[-1]}")
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

columns_needed = ['lastPrice', 'strike', 'expiry', 'impliedVolatility', 'underlying_last','quote_date','T','r','mid_price']
cleaneded_df = df[columns_needed]

cleaneded_df.to_csv(f'./data/cleaned/{ticker_symbol.upper()}.csv', index=False)
print(f"cleaned {ticker_symbol} data and saved to cleaned csv")