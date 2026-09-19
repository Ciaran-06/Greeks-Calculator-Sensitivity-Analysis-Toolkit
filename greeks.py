import numpy as np
import scipy as sp

from scipy.stats import norm

def calculate_d1(S,K,r,vol,T):
    return (np.log(S/K)+(r+(vol**2)/2)*T)/(vol * np.sqrt(T))

def calculate_d2(d1,T,vol):
    return d1 - vol * np.sqrt(T)

def calculate_bs(d1,d2,S,K,r,vol,T):
    return (S * norm.cdf(d1) - K * np.exp(-r * T)*norm.cdf(d2))
def calculate_delta(d1):
    return norm.cdf(d1)
def calculate_vega(d1,S,T):
    return S * np.sqrt(T) * norm.pdf(d1)

if __name__ == "__main__":  
    S=100 
    K=100
    T=1
    r=0.05 
    vol =0.2 
    
    #0.35
    d1 = calculate_d1(S,K,r,vol,T)
    d2 = calculate_d2(d1,T,vol)
    price = calculate_bs(d1, d2, S, K, r, vol, T)
    delta = calculate_delta(d1)
    print(f'd_1: {d1} \nd_2: {d2} \ndelta: {delta}')
    S=110
    K=100 
    T=0.5
    r=0.05 
    vol=0.2
    #0.92
    d1 = calculate_d1(S,K,r,vol,T)
    d2 = calculate_d2(d1,T,vol)
    delta = calculate_delta(d1)
    vega = calculate_vega(d1,S,T)
    price = calculate_bs(d1, d2, S, K, r, vol, T)
    print(f'd_1: {d1} \nd_2: {d2}\ndelta: {delta}')
    epsilon = 0.001
    
    S_up = S + epsilon
    d1_up = calculate_d1(S_up, K, r, vol, T)
    d2_up = calculate_d2(d1_up, T, vol)
    price_up = calculate_bs(d1_up, d2_up, S_up, K, r, vol, T)

    S_down = S - epsilon
    d1_down = calculate_d1(S_down, K, r, vol, T)
    d2_down = calculate_d2(d1_down, T, vol)
    price_down = calculate_bs(d1_down, d2_down, S_down, K, r, vol, T)

    num_delta = (price_up - price_down) / (2 * epsilon)
    
    print(f'Analytical delta: {delta}\nNumerical delta: {num_delta}')
    
    vol_up = vol + epsilon
    d1_up = calculate_d1(S,K,r,vol_up,T)
    d2_up = calculate_d2(d1_up,T,vol_up)
    price_up = calculate_bs(d1_up,d2_up,S,K,r,vol_up,T)
    vol_down = vol - epsilon
    d1_down = calculate_d1(S,K,r,vol_down,T)
    d2_down = calculate_d2(d1_down,T,vol_down)
    price_down = calculate_bs(d1_down,d2_down,S,K,r,vol_down,T)
    
    num_vega = (price_up - price_down) / (2 * epsilon)
    print(f'Analytical Vega: {vega}\nNumerical Vega: {num_vega}')
    
    