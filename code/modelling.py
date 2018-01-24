import numpy as np 

def gaus(x, A, B, C): 
  ''' 
  This is a 3-parameter gaussian function. 
  
  A = amplitude 
  B = centroid 
  C = std. deviation 
  ''' 
  return A * np.exp( -(x - B)**2 / ( 2*C**2))

