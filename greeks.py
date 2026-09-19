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
def calculate_theta(d1,d2,S,K,r,vol,T):
    term1 = -(S * norm.pdf(d1) * vol) / (2 * np.sqrt(T))
    term2 = -r * K * np.exp(-r*T) * norm.cdf(d2)
    return term1 + term2
def calculate_rho(d2,K,r,T):
    return K * T* np.exp(-r*T)*norm.cdf(d2)
def calculate_gamma(d1,S,vol,T):
    return (norm.pdf(d1)) / (S * vol * np.sqrt(T))

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
    vega = calculate_vega(d1,S,T)
    theta = calculate_theta(d1,d2,S,K,r,vol,T)
    rho = calculate_rho(d2,K,r,T)
    gamma = calculate_gamma(d1,S,vol,T)
    epsilon = 0.001
    
    #Perturbing delta
    S_up = S + epsilon
    d1_up = calculate_d1(S_up, K, r, vol, T)
    d2_up = calculate_d2(d1_up, T, vol)
    price_up = calculate_bs(d1_up, d2_up, S_up, K, r, vol, T)
    
    S_down = S - epsilon
    d1_down = calculate_d1(S_down, K, r, vol, T)
    d2_down = calculate_d2(d1_down, T, vol)
    price_down = calculate_bs(d1_down, d2_down, S_down, K, r, vol, T)

    #testing gamma
    price_mid = calculate_bs(d1, d2, S, K, r, vol, T)
    num_gamma = (price_up - 2*price_mid + price_down) / (epsilon**2)
    print(f'Analytical Gamma: {gamma}\nNumerical Gamma: {num_gamma}')
    
    num_delta = (price_up - price_down) / (2 * epsilon)
    
    print(f'Analytical delta: {delta}\nNumerical delta: {num_delta}')
    
    #Perturbing Vevag
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
    
    #Perturbing theta
    T_up = T + epsilon
    d1_up = calculate_d1(S,K,r,vol,T_up)
    d2_up = calculate_d2(d1_up,T_up,vol)
    price_up = calculate_bs(d1_up,d2_up,S,K,r,vol,T_up)
    
    T_down = T - epsilon
    d1_down = calculate_d1(S,K,r,vol,T_down)
    d2_down = calculate_d2(d1_down,T_down,vol)
    price_down = calculate_bs(d1_down,d2_down,S,K,r,vol,T_down)
    
    num_theta = (price_up - price_down) / (2 * epsilon)
    print(f'Analytical Theta: {theta}\nNumerical Theta: {num_theta}')
    
    #Perturbing Rho
    r_up = r + epsilon
    d1_up = calculate_d1(S,K,r_up,vol,T)
    d2_up = calculate_d2(d1_up,T,vol)
    price_up = calculate_bs(d1_up,d2_up,S,K,r_up,vol,T)
    
    r_down = r - epsilon
    d1_down = calculate_d1(S,K,r_down,vol,T)
    d2_down = calculate_d2(d1_down,T,vol)
    price_down = calculate_bs(d1_down,d2_down,S,K,r_down,vol,T)
    
    num_rho = (price_up - price_down) / (2 * epsilon)
    print(f'Analytical Rho: {rho}\nNumerical Rho: {num_rho}') 
    
    