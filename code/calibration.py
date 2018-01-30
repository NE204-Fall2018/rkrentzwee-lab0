import numpy as np
import matplotlib.pyplot as plt 
from modelling import gaus 
from scipy.optimize import curve_fit
from operator import itemgetter  
from scipy.stats import linregress 
import ast 

def loadref(filepath): 
  '''
  load elements and known energy peaks as a list 
  '''
  with open(filepath,'r') as inf: 
    peaks = ast.literal_eval(inf.read()) 
  return peaks 

def loaddata(filepath): 
  '''
  load saved spectra 
  '''
  spectra = np.loadtxt('data/lab0_spectral_data.txt',unpack=True) 
  # TODO: read the source list in from comment line 1 
  source_list = ('Am241', 'Ba133', 'Cs137', 'Co60', 'Eu152') 
  return source_list, spectra

def calibrate(ElementList,source_list,spectra,peaks): 
  '''
  Pass in a list of single-peak elements to use in calibration  
  Return the linear regression for calibration
  Currently only works for elements with a single energy peak  
  '''
  # better would be to look up by element - know number of peaks to search for, fit each 

  # get the reference peak energies  
  cal_peaks = itemgetter(*ElementList)(peaks) 
  # load the spectra for calibration 
  cal_spectra = np.vstack((spectra[source_list.index(ElementList[0])],spectra[source_list.index(ElementList[1])])) 

  # find and fit the peak in each spectra 
  centroids = []   
  for item in cal_spectra: 
#    plt.plot(item) 
    a0 = np.max(item) 
    b0 = np.argmax(item) 
    c0 = 3 
    p0 = (a0, b0, c0) 
    width = range(b0-(2*c0),b0+1+(2*c0))
    counts = item[b0-(2*c0):b0+1+(2*c0)]
    popt, pcov = curve_fit(gaus,width,counts,p0=p0)
    width2 = np.arange(b0-(2*c0),b0+1+(2*c0),0.1)
#    plt.plot(width2,gaus(width2,*popt))
    # automate a zoomed in image of fit
    centroids.append(popt[1]) 
  
  # fit a linear regression to the saved centroids and the reference peak energies 
  m, b, _, _, _ = linregress(centroids, cal_peaks)
  return m, b 

def validate(Element,m,b,source_list,spectra,peaks): 
  '''
  given an element name, returns the percent error for each energy peak 
  
  Input: 
  Element: source ID as a string
  m, b: variables from calibration (linear regression fit)

  Returns: 
  tuples of true energy peak, calibrated peak, and percent error 
  ''' 
  spectrum = spectra[source_list.index(Element)]
#  plt.plot(spectrum)  
  TruePeaks = peaks[Element] 
  obs_peak = []
  errors = np.empty([len(TruePeaks),3]) 
#  header = np.array(['True Peak Energy','Observed Peak Energy', 'Relative Error']) 
  # search for peaks in spectra near the true peak values 
  for i in TruePeaks: 
    b0 = int((i-b)/m)
    a0 = spectrum[b0]
    c0 = 4  
    p0 = (a0, b0, c0) 
    width = range(b0-(2*c0),b0+1+(2*c0))
    counts = spectrum[b0-(2*c0):b0+1+(2*c0)]
    popt, pcov = curve_fit(gaus,width,counts,p0=p0)
    width2 = np.arange(b0-(2*c0),b0+1+(2*c0),0.1)
#    plt.plot(width2,gaus(width2,*popt))
    obs_peak.append(popt[1]*m + b)

  #calculate the percent error for each value 
  for i in range(len(obs_peak)): 
     relerr = 100 * (abs(TruePeaks[i] - obs_peak[i])/TruePeaks[i])
     errors[i] = [TruePeaks[i], obs_peak[i],relerr]
  # save final as text file for table? Save as image for table?
  np.savetxt('validation%s.csv' % str(Element), errors, delimiter=' & ', fmt='%.3f', newline=' \\\\\n') 
  return errors
