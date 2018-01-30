import numpy as np 
import calibration as cal 

m, b = cal.calibrate(['Am241','Cs137'])
cal.validate('Ba133',m,b) 

