import numpy as np
import scipy as sp

ticker = "SPY"
d1 = None
def calculateD1():
    print('Calculating d_1')
    d1 = 1
    return d1
    
def calculateDelta(call = True, ):
    print(f'Calculating Delta for {ticker}')
    
    if d1 is None:
        calculateD1()
    
    
        
    
    