''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-01-30 by Will Bowman. This script takes the simultaneous EDX and
 EELS results and calculates Ca/Ce and O/Ce k-factors.
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
# import pandas as pd
# import csv, imp, os

##


''' ########################### USER-DEFINED ########################### '''

data_path_10Ca = 'C:/Crozier_Lab/Writing/2015_conductvity and chemistry of CaDC grain boundaries/EDX_EELS_quantities_10Ca.txt'
data_path_CeO2_STD = 'C:/Crozier_Lab/Writing/2015_conductvity and chemistry of CaDC grain boundaries/150130_CeO2_crushed_STD_quantification_results.txt'
k_Ca_Ce_EDX, stdev_k_Ca_Ce_EDX = 2.3308, 0.3281 # from sampele '150122 ethanol + sonicate + dip holey C'
C_Ce_std, C_O_std = 0.33, 0.66


''' ########################### FUNCTIONS ########################### '''


''' ########################### MAIN SCRIPT ########################### '''

# READ DATA FILES
# read 10Ca quantification results
d = np.genfromtxt( data_path_10Ca, skiprows=1, delimiter='\t' )
spec_name, I_CaL_EDX, uI_CaL_EDX, snI_CaL_EDX, I_CeL_EDX, uI_CeL_EDX, snI_CeL_EDX, tL, I_CaL_EEL, uI_CaL_EEL, I_OK_EEL, uI_OK_EEL, I_CeM_EEL, uI_CeM_EEL = d.T

# read CeO2_STD quantification results
d_std = np.genfromtxt( data_path_CeO2_STD, skiprows = 1, delimiter = '\t' )
tL_std, I_OK_EEL_std, uI_OK_EEL_std, I_CeM_EEL_std, uI_CeM_EEL_std = d_std.T

# CALCULATE QUANTITIES
C_O_Ce_std = C_O_std / C_Ce_std # O/Ce std molar concentration ratio
I_O_Ce_std_EEL = I_OK_EEL_std / I_CeM_EEL_std # O/Ce std integrated intensity ratio
k_O_Ce_std_EEL = C_O_Ce_std / I_O_Ce_std_EEL

I_Ca_Ce_EDX = I_CaL_EDX / I_CeL_EDX # Ca/Ce integrated intensity ratio
C_Ca_Ce_EDX = I_Ca_Ce_EDX * k_Ca_Ce_EDX # elemental concentration ratio
C_Ca = C_Ca_Ce_EDX / ( 1 + C_Ca_Ce_EDX ) # [Ca], assume [Ca] + [Ce] = 1
C_Ce = 1 - C_Ca

# calculate eels k-factor for each acquisition from EDX composition
# C_Ca/C_Ce / (I_Ca/I_Ce) = k_eels
I_Ca_Ce_EEL = I_CaL_EEL / I_CeM_EEL # Ca/Ce eels integrated intensity ratio
k_Ca_Ce_EEL = C_Ca_Ce_EDX / I_Ca_Ce_EEL

# PLOT STUFF
pl.close( 'all' )
# pl.plot( I_Ca_Ce_EDX, color='k' )
pl.plot( k_O_Ce_std_EEL, color='g' )
pl.plot( k_Ca_Ce_EEL, color = 'b' )

pl.figure()
# pl.scatter( tL, I_Ca_Ce_EDX, color='k' )
pl.scatter( tL_std, k_O_Ce_std_EEL, color='g' )
pl.scatter( tL, k_Ca_Ce_EEL, color = 'b' )

''' ########################### REFERENCES ########################### '''