import pandas as pd
import greeks as gr
import sys

if len(sys.argv) < 2:
    print('Usage: python main.py <ticker>')
    sys.exit(1)

ticker_symbol = sys.argv[1].upper()

df = pd.read_csv(f'./data/cleaned/{ticker_symbol}.csv')

print(f"Loaded {len(df)} records for {ticker_symbol}")

#calculate Black-Scholes-Merton
df['d1'] = df.apply(lambda row: gr.calculate_d1(row['underlying_last'],row['strike'],row['r'],row['impliedVolatility'],row['T']), axis=1)
df['d2'] = df.apply(lambda row: gr.calculate_d2(row['d1'],row['T'],row['impliedVolatility']), axis=1)
df['bs'] = df.apply(lambda row: gr.calculate_bs(row['d1'],row['d2'],row['underlying_last'],row['strike'],row['r'],row['impliedVolatility'],row['T']),axis=1)

#calculating greeks
df['delta'] = df.apply(lambda row: gr.calculate_delta(row['d1']), axis=1)
df['vega'] = df.apply(lambda row: gr.calculate_vega(row['d1'],row['underlying_last'],row['T']), axis=1)
df['theta'] = df.apply(lambda row: gr.calculate_theta(row['d1'],row['d2'],row['underlying_last'],row['strike'],row['r'],row['impliedVolatility'],row['T']), axis=1)
df['rho'] = df.apply(lambda row: gr.calculate_rho(row['d2'],row['strike'],row['r'],row['T']), axis=1)
df['gamma'] = df.apply(lambda row: gr.calculate_gamma(row['d1'],row['underlying_last'],row['impliedVolatility'],row['T']), axis=1)

# Save calculated Greeks
df.to_csv(f'./data/calculated/{ticker_symbol}_greeks.csv', index=False)
print(f"Saved Greeks to ./data/calculated/{ticker_symbol}_greeks.csv")

# Sensitivity check
print(f"\nGreeks summary (first 5 rows):")
print(df[['delta', 'vega', 'theta', 'rho', 'gamma']].head())
print(f"\nGreeks statistics:")
print(df[['delta', 'vega', 'theta', 'rho', 'gamma']].describe())

df['moneyness'] = df['strike'] / df['underlying_last']
