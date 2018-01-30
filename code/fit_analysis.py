# IPython log file
import numpy as np 
from code.modelling import gaus
from scipy.optimize import curve_fit
samples = np.random.normal(100,2,1000) 
v, be, _ = plt.hist(samples, bins=20, histtype="step"); 
v
be
v.shape
be.shape
bc = be[:-1] + np.diff(be)[0]/2. 
plot(bc,v, 'o')
curve_fit(gaus,bc,v)
a0 = np.max(v)
b0 = bc[np.argmax(v)]
c0 = 2
p0 = (a0, b0, c0)
curve_fit(gaus,bc,v,p0=p0)
popt, pcov = curve_fit(gaus,bc,v,p0=p0)
plot(gaus(popt)) 
