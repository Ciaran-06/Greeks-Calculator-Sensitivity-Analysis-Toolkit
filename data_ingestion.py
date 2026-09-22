import pandas as pd
import databento as db

from tabulate import tabulate

import sys
import csv
import os

from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python data_ingestion.py <ticker>")
    sys.exit(1)

print('Starting Data Ingestion...')
ticker_symbol = sys.argv[1].upper()

#db.DBNStore.from_file(path).to_df()

ticker_symbol = sys.argv[1].upper()
data = []     
print('Iterating Through Files...')
for regime in ['low_vol', 'high_vol']:
    for file in os.listdir(f'./data/unproccesed/{ticker_symbol}/{regime}'):
        filename = os.fsdecode(file)
        print(f'Working on {filename}...')
        if filename.endswith('dbn.zst'):
            current_data = db.DBNStore.from_file(f'./data/unproccesed/{ticker_symbol}/{regime}/{filename}').to_df()
            current_data['regime'] = regime
            current_data = current_data.sort_values('ts_event')
            current_data['date'] = current_data['ts_event'].dt.normalize() 
            current_data = current_data.drop_duplicates(subset=['symbol', 'date'], keep='last')
            data.append(current_data)

df = pd.concat(data, ignore_index=True)

#Index(['ts_event', 'rtype', 'publisher_id', 'instrument_id', 'side', 'price',
#       'size', 'flags', 'bid_px_00', 'ask_px_00', 'bid_sz_00', 'ask_sz_00',
#       'bid_pb_00', 'ask_pb_00', 'symbol', 'regime'],
#      dtype='str') 
df['date'] = df['ts_event'].dt.tz_localize(None).dt.normalize()
df['mid_price'] = (df['bid_px_00'] + df['ask_px_00']) / 2
df['strike'] = (df['symbol'].str[-8:]).astype(float)/1000
df['type'] = df['symbol'].str[-9]
df['expiry'] = df['symbol'].str[-15:-9]
df['expiry'] = pd.to_datetime(df['expiry'], format='%y%m%d')
df['T'] = (df['expiry'] - df['date']).dt.days / 365
print(df.head(10))
print(len(df))    

os.makedirs(f'./data/uncleaned/{ticker_symbol}', exist_ok=True)
df.to_csv(f'./data/uncleaned/{ticker_symbol}/{ticker_symbol}.csv', index=False)