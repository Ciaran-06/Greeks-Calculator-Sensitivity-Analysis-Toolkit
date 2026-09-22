import pandas as pd
import databento as db

import sys
import csv
import os

from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python data_ingestion.py <ticker>")
    sys.exit(1)

print('Starting Data Ingestion...')
ticker_symbol = sys.argv[1].upper()

folder = Path('./data/uncleaned')
new_folder = ticker_symbol
new_path = folder / new_folder
#db.DBNStore.from_file(path).to_df()

if len(sys.argv) < 2:
    print("Usage: python data_ingestion.py <ticker>")
    sys.exit(1)

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
            data.append(current_data)

df = pd.concat(data, ignore_index=True)

print(df.columns)