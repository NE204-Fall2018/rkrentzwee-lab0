import numpy as np
import matplotlib.pyplot as plt 
from modelling import gaus 
from scipy.optimize import curve_fit
from operator import itemgetter  
from scipy.stats import linregress 

# Dictionary of known energy peaks for some elements  
# Ref: S.Y.F. Chu, L.P. Ekstro m, and R. B. Firestone, The Lund/LBNL Nuclear Data Search, v. 2.0, Feb. 1999, http://nucleardata.nuclear.lu.se/nucleardata/toi/. 
peaks = {'Am241':(59.5412),
         'Ba133':(80.8983,276.398,302.853,356.017,383.851), 
         'Cs137':(661.657),
         'Co69':(1173.237,1332.501), 
         'Eu152':(121.7817,244.6975,344.2785,411.1163,778.9040,867.373,964.079,1085.869,1112.069,1212.948,1299.140,1408.006), 
         'Cd109':(88.04), 
         'Th228':(238.6,583.2,2614.5)} 

# load saved spectra 
spectra = np.loadtxt('data/lab0_spectral_data.txt',unpack=True) 
# TODO: read the source list in from comment line 1 
source_list = ('Am241', 'Ba133', 'Cs137', 'Co60', 'Eu152') 

def calibrate(ElementList): 
  '''
  Pass in a list of single-peak elements to use in calibration  
  Return the linear regression for calibration 
  '''
  # better would be to look up by element - find number of peaks to search for, 

  #cal_peaks = (peaks[source_list[0]], peaks[source_list[2]]) 
  cal_peaks = itemgetter(*ElementList)(peaks) 
  cal_spectra = np.vstack((spectra[source_list.index(ElementList[0])],spectra[source_list.index(ElementList[1])])) 
  centroids = [] 
  
  for item in cal_spectra: 
    plt.plot(item) 
    a0 = np.max(item) 
    b0 = np.argmax(item) 
    c0 = 3 
    p0 = (a0, b0, c0) 
    width = range(b0-(2*c0),b0+1+(2*c0))
    counts = item[b0-(2*c0):b0+1+(2*c0)]
    popt, pcov = curve_fit(gaus,width,counts,p0=p0)
    width2 = np.arange(b0-(2*c0),b0+1+(2*c0),0.1)
    plt.plot(width2,gaus(width2,*popt))
    # automate a zoomed in image of fit
    centroids.append(popt[1]) 
  
  m, b, _, _, _ = linregress(centroids, cal_peaks)
  return m, b 

# now validate by finding centroids and comparing calculated energy w real peaks 
# get relative maxima, apply gaussian to find centroids, compare with actual 
def validate(Element,m,b): 
  '''
  given an element name, returns the percent error for each energy peak 
  
  Input: 
  Element: source ID as a string
  m, b: variables from calibration (linear regression fit)

  Returns: 
  tuples of true energy peak, calibrated peak, and percent error 
  ''' 
  spectrum = spectra[source_list.index(Element)]
  plt.plot(spectrum)  
  TruePeaks = peaks[Element] 
  obs_peak = []
  final = [('True Peak Energy','Observed Peak Energy', 'Relative Error')] 
  # search for peaks in spectra, guessing they're near the true peak value 
  for i in TruePeaks: 
    b0 = int((i-b)/m)
    a0 = spectrum[b0]
    c0 = 4  
    p0 = (a0, b0, c0) 
    width = range(b0-(2*c0),b0+1+(2*c0))
    counts = spectrum[b0-(2*c0):b0+1+(2*c0)]
    popt, pcov = curve_fit(gaus,width,counts,p0=p0)
    width2 = np.arange(b0-(2*c0),b0+1+(2*c0),0.1)
    plt.plot(width2,gaus(width2,*popt))
    obs_peak.append(popt[1]*m + b)
  for i in range(len(obs_peak)): 
     relerr = abs(TruePeaks[i] - obs_peak[i])/TruePeaks[i] 
     final.append((TruePeaks[i], obs_peak[i],relerr)) 
  # save final as text file for table? Save as image for table? 
  return final 
