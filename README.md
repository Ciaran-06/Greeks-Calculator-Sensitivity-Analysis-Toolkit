# Greeks Calculator & Sensitivity Analysis Toolkit

A Python toolkit for computing Black-Scholes-Merton option Greeks on real market data and analysing which inputs drive option prices. Built as a companion to my research on improving the predictive power of the Black-Scholes-Merton model.

**Status:** data pipeline complete · Greeks calculator in progress

## Overview

The toolkit pulls live SPY call option chains, cleans them, and (in progress) computes Delta, Gamma, Vega, Theta and Rho for every contract using fully vectorised NumPy — no Python loops.

## Project Structure

```
.
├── data_ingestion.py   # Fetches option chains + risk-free rate, cleans, saves CSVs
├── greeks.py           # Vectorised Greeks functions (in progress)
├── main.py             # Entry point: loads cleaned data for a ticker
└── data/               # Generated locally, not committed
    ├── uncleaned/
    ├── cleaned/
    └── calculated/
```

## Usage

```bash
pip install yfinance pandas numpy scipy
python data_ingestion.py SPY
python main.py SPY
```

## Data Pipeline

**Sources (via `yfinance`):**
- Call option chains for every listed expiry
- Spot price: last close of the underlying
- Risk-free rate: 13-week US T-bill yield (`^IRX`)

**Derived fields:**
- `mid_price` — average of bid and ask (more current than last traded price)
- `T` — time to expiry in years, measured from the last trading day rather than the run date, so weekend runs don't overstate T
- `r` — risk-free rate as a decimal

**Cleaning filters** (example run, SPY, September 2026):

| Filter | Reason | Rows removed |
|---|---|---|
| Bid > 0 | No active market | 377 |
| Implied vol > 1% | yfinance returns near-zero IV when it can't compute one | 129 |
| T ≥ 7 days | IV is unstable very close to expiry | 195 |
| Moneyness (K/S) in [0.8, 1.2] | Deep ITM/OTM quotes give unreliable IV | 1,496 |
| **Total** | 4,632 → **2,435** | **2,197** |

## Model

Greeks are computed under Black-Scholes-Merton for European calls:

- d₁ = [ln(S/K) + (r + σ²/2)T] / (σ√T),  d₂ = d₁ − σ√T
- Δ = N(d₁)
- Γ = φ(d₁) / (Sσ√T)
- Vega = S φ(d₁) √T
- Θ = −S φ(d₁) σ / (2√T) − rK e^(−rT) N(d₂)
- ρ = K T e^(−rT) N(d₂)

## Roadmap

- [x] Data ingestion and cleaning
- [ ] **Phase 1:** vectorised Greeks with edge-case handling (T → 0)
- [ ] **Phase 2:** volatility smile fitting and interpolation (SciPy)
- [ ] **Phase 3:** Pandas pipeline computing Greeks per expiry
- [ ] **Phase 4:** sensitivity report ranking which inputs drive prices

## Limitations

- Single snapshot: `yfinance` provides current chains only, so analysis is grouped by expiry rather than by date.
- Calls only; SPY dividends are currently ignored.
- `^IRX` is a discount-basis yield, used as an approximation to the continuously compounded rate.

## License

See [LICENSE](LICENSE).
