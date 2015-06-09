''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-06-02 by Will Bowman. This script calculates defect profiles 
 according to Guoy-Chapman model [Tuller, Bishop chapter] (see eq. 13).
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import csv, imp, os

##


''' ########################### USER-DEFINED ########################### '''
# CONSTANTS #
e, k_b = 1, 8.62e-05 # eV, eV/K
C_bulk = [ 0.02, 0.05, 0.1 ] # mol
C_0 = [ 0.15, 0.4, 0.45 ] # mol
z = -2 # Ca2+ is -2 relative to Ce4+
# Dphi = 0.4 # V
T = 300  # K
# distance_max = 10 # nm from gb core
# distance = np.linspace( 0, distance_max )
# # _data_path = '' # path to data file


''' ########################### FUNCTIONS ########################### '''

    
''' ########################### MAIN SCRIPT ########################### '''
# _data = np.loadtxt( _data_path, skiprows = 3 ) # read data, ignore first three rows

# C_0 = ( np.exp( -e * Dphi / ( k_b * T ) ) ) ** z * C_bulk
# print( C_0 )

for i, c_0 in enumerate( C_0 ):
    dPhi_0 = np.log( ( c_0 / C_bulk[ i ] ) ** ( 1 / z ) ) * k_b * T / -e
    print( dPhi_0 )

    
''' ########################### REFERENCES ########################### '''