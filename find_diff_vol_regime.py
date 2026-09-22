import yfinance as yf

vix = yf.Ticker("^VIX").history(start="2021-01-01", end="2026-09-20")
print(vix['Close'].quantile([0.1, 0.9]))

print(vix[vix['Close'] > 26.5].index)  
print(vix[vix['Close'] < 13.8].index)  

high = vix[vix['Close'] > 26.5]
counts = high.groupby([high.index.year, high.index.month]).size()
print(counts.sort_values(ascending=False).head(10))

calm = vix[vix['Close'] < 13.8]
print(calm.groupby([calm.index.year, calm.index.month]).size().sort_values(ascending=False).head(10))