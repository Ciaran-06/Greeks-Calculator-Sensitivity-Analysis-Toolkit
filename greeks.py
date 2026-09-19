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

if __name__ == "__main__":  
    S=100 
    K=100
    T=1
    r=0.05 
    vol =0.2 
    #0.35
    d1 = calculate_d1(S,K,r,vol,T)
    d2 = calculate_d2(d1,T,vol)
    delta = calculate_delta(d1)
    price = calculate_bs(d1, d2, S, K, r, vol, T)
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
    price = calculate_bs(d1, d2, S, K, r, vol, T)
    print(f'd_1: {d1} \nd_2: {d2}\ndelta: {delta}')
    
    