import numpy as np 
import calibration as cal 

peaks = cal.loadref('code/sourcedict.txt')
source_list, spectra = cal.loaddata('data/lab0_spectral_data.txt') 
m, b = cal.calibrate(['Am241','Cs137'],source_list,spectra,peaks)
cal.validate('Ba133',m,b,source_list,spectra,peaks) 

