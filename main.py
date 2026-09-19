import pandas as pd
import greeks as gr
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:
    print('Usage: python main.py <ticker>')
    sys.exit(1)

ticker_symbol = sys.argv[1].upper()

df = pd.read_csv(f'./data/cleaned/{ticker_symbol}.csv')

print(f"Loaded {len(df)} records for {ticker_symbol}")

#casting columuns into arrays to allow for vecotrisation and improve run-time
spot_price = df['underlying_last'].values
strike_price = df['strike'].values
time_to_expiry = df['T'].values
volatility = df['impliedVolatility'].values
risk_free_rate = df['r'].values

#calculate Black-Scholes-Merton
d1_array = gr.calculate_d1(spot_price,strike_price,risk_free_rate,volatility,time_to_expiry)
d2_array = gr.calculate_d2(d1_array,time_to_expiry,volatility)
bs_array = gr.calculate_bs(d1_array,d2_array,spot_price,strike_price,risk_free_rate,volatility,time_to_expiry)

#calculate greeks
delta_array = gr.calculate_delta(d1_array)
vega_array = gr.calculate_vega(d1_array,spot_price,time_to_expiry)
theta_array = gr.calculate_theta(d1_array,d2_array,spot_price,strike_price,risk_free_rate,volatility,time_to_expiry)
rho_array = gr.calculate_rho(d2_array,strike_price,risk_free_rate,time_to_expiry)
gamma_array = gr.calculate_gamma(d1_array,spot_price,volatility,time_to_expiry)

#putting results back into df
df['d1'] = d1_array
df['d2'] = d2_array
df['bs'] = bs_array
df['delta'] = delta_array
df['vega'] = vega_array
df['theta'] = theta_array
df['rho'] = rho_array
df['gamma'] = gamma_array

# Save calculated Greeks
df.to_csv(f'./data/calculated/{ticker_symbol}_greeks.csv', index=False)
print(f"Saved Greeks to ./data/calculated/{ticker_symbol}_greeks.csv")

# Sensitivity check
print(f"\nGreeks summary (first 5 rows):")
print(df[['delta', 'vega', 'theta', 'rho', 'gamma']].head())
print(f"\nGreeks statistics:")
print(df[['delta', 'vega', 'theta', 'rho', 'gamma']].describe())

df['moneyness'] = df['strike'] / df['underlying_last']
moneyness_boundaries = [0.8, 0.9, 1.0, 1.1, 1.2]
moneyness_labels = ["0.80-0.90", "0.90-1.00", "1.00-1.10", "1.10-1.20"]
df['moneyness_bin'] = pd.cut(df['moneyness'], moneyness_boundaries, moneyness_labels)

df.groupby('moneyness_bin')
sensitivity_table = df.groupby('moneyness_bin')[['delta', 'vega', 'theta', 'gamma', 'rho']].agg(['mean', 'std'])
sensitivity_table.columns = ['_'.join(col).strip() for col in sensitivity_table.columns.values]
sensitivity_table.to_csv('./data/calculated/sensitivity_by_moneyness.csv')

df.groupby('expiry')
single_day_info = df[df['expiry'] == '2026-09-25']
print(single_day_info)
plt.plot(single_day_info['strike'], single_day_info['impliedVolatility'])
plt.xlabel("Strike Price")
plt.ylabel("Implied Volatility")
plt.title("Volatility Smile")
plt.show()

vol_over_single_day = single_day_info['impliedVolatility']

