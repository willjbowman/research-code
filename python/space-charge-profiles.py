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
C_0 = [ 0.17, 0.47, 0.4 ] # mol
z = -2 # Ca2+ is -2 relative to Ce4+
# Dphi = 0.4 # V

T_C = np.linspace( 25, 2000, 20 ) # K
# distance_max = 10 # nm from gb core
# distance = np.linspace( 0, distance_max )
# # _data_path = '' # path to data file


''' ########################### FUNCTIONS ########################### '''

    
''' ########################### MAIN SCRIPT ########################### '''
# _data = np.loadtxt( _data_path, skiprows = 3 ) # read data, ignore first three rows

# C_0 = ( np.exp( -e * Dphi / ( k_b * T ) ) ) ** z * C_bulk
# print( C_0 )
T_K = np.transpose( T_C + 273 )
dPhi_0_2, dPhi_0_5, dPhi_0_10 = [], [], []
for i, T in enumerate( T_K ):
    dPhi_0_i = np.log( ( C_0[ 0 ] / C_bulk[ 0 ] ) ** ( 1 / z ) ) * k_b * T / -e
    # print( dPhi_0_i )
    dPhi_0_2 = np.append( dPhi_0_2, dPhi_0_i )
    
for i, T in enumerate( T_K ):
    dPhi_0_i = np.log( ( C_0[ 1 ] / C_bulk[ 1 ] ) ** ( 1 / z ) ) * k_b * T / -e
    # print( dPhi_0_i )
    dPhi_0_5 = np.append( dPhi_0_5, dPhi_0_i )
    
for i, T in enumerate( T_K ):
    dPhi_0_i = np.log( ( C_0[ 2 ] / C_bulk[ 2 ] ) ** ( 1 / z ) ) * k_b * T / -e
    # print( dPhi_0_i )
    dPhi_0_10 = np.append( dPhi_0_10, dPhi_0_i )

T_C_T = np.transpose( T_C )

pl.figure()
pl.plot( T_C_T, dPhi_0_2, T_C_T, dPhi_0_5, T_C_T, dPhi_0_10 )
pl.legend( ( '2 mol%', '5 mol%', '10 mol%' ), loc = 'lower right' )
    
# dPhi_0 = np.empty( ( len( C_0 ) - 1 , len( T_K ) - 1 ) )
# for i, C in enumerate( C_0 ):
#     for j, T in enumerate( T_K ):
#         dPhi_0[ j ][ i ] = np.log( ( C / C_bulk[ i ] ) ** ( 1 / z ) ) * k_b * T / -e
#         # print( i, j, C, T )
#         # print( np.log( ( C / C_bulk[ i ] ) ** ( 1 / z ) ) * k_b * T / -e )
# 
# for row in dPhi_0:
#     pl.plot( T_K, row )

    
''' ########################### REFERENCES ########################### '''