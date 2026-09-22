import pandas as pd
import numpy as np 
import seaborn as sea
import greeks as gr

import sys
import os

if len(sys.argv) < 2:
    print("Usage: python data_ingestion.py <ticker>")
    sys.exit(1)

ticker_symbol = sys.argv[1].upper()
df = pd.read_csv(f'./data/uncleaned/{ticker_symbol}/{ticker_symbol}.csv')

old_df_len = len(df)
#remove missing/zero quotes
df = df[df['bid_px_00'] > 0]
df = df[df['ask_px_00'] > 0]

#remove locked quotes
df = df[df['bid_px_00'] < df['ask_px_00']]

#remove dust options
df = df[df['mid_price'] > 0.05]

#remove insane spreads
df['spread'] = (df['ask_px_00'] - df['bid_px_00']) / df['mid_price']
df = df[df['spread'] < 0.5]

#remove short dated options
df = df[df['T'] >= 7/365]

#remove put options
df = df[df['type'] == 'C']

#Arb Filter
intrinsic = np.maximum(0, df['underlying_last'] - df['strike'] * np.exp(-df['r'] * df['T']))
df = df[df['mid_price'] >= intrinsic]

df['impliedVolatility'] = df.apply(
    lambda row: gr.calculate_iv(row['underlying_last'], row['strike'], row['T'], row['r'], row['mid_price']),
    axis=1
)

#moneyness column
df['moneyness'] = df['strike'] / df['underlying_last']
df = df[df['moneyness'].between(0.8, 1.2)]

cleaned_df = len(df)
print(df[['r','underlying_last']].isna().sum())
print(f'Removed {old_df_len - cleaned_df} of Bad/Invalid Quotes')

os.makedirs(f'./data/cleaned/{ticker_symbol}', exist_ok=True)
df.to_csv(f'./data/cleaned/{ticker_symbol}/{ticker_symbol}.csv', index=False)
