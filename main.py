import pandas as pd
import sys

if len(sys.argv) < 2:
    print('Usage: python main.py <ticker>')
    sys.exit(1)

ticker_symbol = sys.argv[1].upper()

df = pd.read_csv(f'./data/cleaned/{ticker_symbol}.csv')

print(f"Loaded {len(df)} records for {ticker_symbol}")

    