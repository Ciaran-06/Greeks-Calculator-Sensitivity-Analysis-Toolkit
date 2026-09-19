import numpy as np
from scipy.stats import norm

import greeks

# ---------------------------------------------------------------------------
# Reference price: an independent BS call price used as the "oracle" for the
# finite-difference checks. Deliberately written separately from greeks.py,
# so a bug in your d1 can't also hide in the thing checking it.
# ---------------------------------------------------------------------------
def ref_call_price(S, K, T, r, vol):
    d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


# ---------------------------------------------------------------------------
# ADAPTERS: translate a standard (S, K, T, r, vol) call into YOUR signatures.
# If you change a function's arguments, only edit the matching line here.
# Returns None if you haven't written that function yet.
# ---------------------------------------------------------------------------
def _get(name):
    return getattr(greeks, name, None)

def d1(S, K, T, r, vol):
    return greeks.calculate_d1(S, K, r, vol, T)

def d2(S, K, T, r, vol):
    return greeks.calculate_d2(d1(S, K, T, r, vol), T, vol)

def delta(S, K, T, r, vol):
    return greeks.calculate_delta(d1(S, K, T, r, vol))

def gamma(S, K, T, r, vol):
    f = _get("calculateGamma")
    return None if f is None else f(d1(S, K, T, r, vol), S, vol, T)

def vega(S, K, T, r, vol):
    f = _get("calculateVega")
    return None if f is None else f(d1(S, K, T, r, vol), S, T)

def theta(S, K, T, r, vol):
    f = _get("calculateTheta")
    if f is None:
        return None
    return f(d1(S, K, T, r, vol), d2(S, K, T, r, vol), S, K, T, r, vol)

def rho(S, K, T, r, vol):
    f = _get("calculateRho")
    return None if f is None else f(d2(S, K, T, r, vol), K, T, r)


# ---------------------------------------------------------------------------
# Tiny test runner (no pytest needed)
# ---------------------------------------------------------------------------
results = {"PASS": 0, "FAIL": 0, "SKIP": 0}

def check(name, got, expected, tol=1e-4):
    if got is None:
        results["SKIP"] += 1
        print(f"  SKIP  {name:<42} (not written yet)")
        return
    ok = np.allclose(got, expected, atol=tol)
    results["PASS" if ok else "FAIL"] += 1
    tag = "PASS" if ok else "FAIL"
    if np.ndim(got) == 0:
        print(f"  {tag}  {name:<42} got {float(got):.6f}  expected {float(expected):.6f}")
    else:
        worst = np.max(np.abs(np.asarray(got) - np.asarray(expected)))
        print(f"  {tag}  {name:<42} max error {worst:.2e}")

def check_true(name, condition_fn, value):
    if value is None:
        results["SKIP"] += 1
        print(f"  SKIP  {name:<42} (not written yet)")
        return
    ok = bool(np.all(condition_fn(np.asarray(value))))
    results["PASS" if ok else "FAIL"] += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")


# ---------------------------------------------------------------------------
# 1. Known values
# ---------------------------------------------------------------------------
print("\n1. Known values")

# Your own two cases from earlier
check("d1  (S=100 K=100 T=1 r=5% vol=20%)", d1(100, 100, 1, 0.05, 0.2), 0.35)
check("d2  (S=100 K=100 T=1 r=5% vol=20%)", d2(100, 100, 1, 0.05, 0.2), 0.15)
check("delta (S=100 K=100 T=1)",            delta(100, 100, 1, 0.05, 0.2), 0.636831)
check("d1  (S=110 K=100 T=0.5)",            d1(110, 100, 0.5, 0.05, 0.2), 0.921432)
check("d2  (S=110 K=100 T=0.5)",            d2(110, 100, 0.5, 0.05, 0.2), 0.780011)
check("delta (S=110 K=100 T=0.5)",          delta(110, 100, 0.5, 0.05, 0.2), 0.821588)

# Hull's standard textbook example: S=42, K=40, r=10%, vol=20%, T=0.5
check("Hull d1",    d1(42, 40, 0.5, 0.10, 0.2),    0.769263)
check("Hull d2",    d2(42, 40, 0.5, 0.10, 0.2),    0.627841)
check("Hull delta", delta(42, 40, 0.5, 0.10, 0.2), 0.779131)
check("Hull price (reference fn sanity)", ref_call_price(42, 40, 0.5, 0.10, 0.2), 4.7594)


# ---------------------------------------------------------------------------
# 2. Properties that must hold for any input
# ---------------------------------------------------------------------------
print("\n2. Properties (on a grid of 1,000 random options)")

rng = np.random.default_rng(0)
n = 1000
S   = rng.uniform(50, 150, n)
K   = S * rng.uniform(0.8, 1.2, n)   # same moneyness range as your cleaned data
T   = rng.uniform(0.05, 2.0, n)
r   = rng.uniform(0.0, 0.08, n)
vol = rng.uniform(0.05, 0.6, n)

check_true("functions accept whole arrays (vectorised)",
           lambda x: x.shape == (n,), delta(S, K, T, r, vol))
check_true("call delta is between 0 and 1",
           lambda x: (x > 0) & (x < 1), delta(S, K, T, r, vol))
check_true("d2 < d1 always (d2 = d1 - vol*sqrt(T))",
           lambda x: x > 0, d1(S, K, T, r, vol) - d2(S, K, T, r, vol))
check_true("gamma is positive",  lambda x: x > 0, gamma(S, K, T, r, vol))
check_true("vega is positive",   lambda x: x > 0, vega(S, K, T, r, vol))
check_true("call rho is positive", lambda x: x > 0, rho(S, K, T, r, vol))

check_true("deep ITM delta -> 1  (S=200, K=100)",
           lambda x: x > 0.99, delta(200, 100, 0.25, 0.05, 0.2))
check_true("deep OTM delta -> 0  (S=50,  K=100)",
           lambda x: x < 0.01, delta(50, 100, 0.25, 0.05, 0.2))


# ---------------------------------------------------------------------------
# 3. Finite differences: each Greek vs the slope of the price
#    Central difference: (price(x+h) - price(x-h)) / 2h
#    Units assumed: per 1.00 of vol, per 1.00 of r, per YEAR for theta.
#    If you scale vega /100 or theta /365, scale `expected` to match.
# ---------------------------------------------------------------------------
print("\n3. Finite differences (Greek vs numerical derivative of price)")

h = 1e-4
P = ref_call_price

fd_delta = (P(S + h, K, T, r, vol) - P(S - h, K, T, r, vol)) / (2 * h)
fd_gamma = (P(S + h, K, T, r, vol) - 2 * P(S, K, T, r, vol) + P(S - h, K, T, r, vol)) / h**2
fd_vega  = (P(S, K, T, r, vol + h) - P(S, K, T, r, vol - h)) / (2 * h)
# Theta is the derivative w.r.t. calendar time passing, i.e. MINUS dP/dT
fd_theta = -(P(S, K, T + h, r, vol) - P(S, K, T - h, r, vol)) / (2 * h)
fd_rho   = (P(S, K, T, r + h, vol) - P(S, K, T, r - h, vol)) / (2 * h)

check("delta vs finite difference", delta(S, K, T, r, vol), fd_delta, tol=1e-5)
check("gamma vs finite difference", gamma(S, K, T, r, vol), fd_gamma, tol=1e-3)
check("vega  vs finite difference", vega(S, K, T, r, vol),  fd_vega,  tol=1e-4)
check("theta vs finite difference", theta(S, K, T, r, vol), fd_theta, tol=1e-4)
check("rho   vs finite difference", rho(S, K, T, r, vol),   fd_rho,   tol=1e-4)


# ---------------------------------------------------------------------------
print(f"\n{results['PASS']} passed, {results['FAIL']} failed, {results['SKIP']} skipped\n")