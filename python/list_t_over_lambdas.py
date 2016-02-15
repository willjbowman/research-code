''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-02-18 by Will Bowman. This takes t_over_lambda_raw_DM_output.txt 
 and creates a list of file names and t/lambda values calculated from low-loss
 EELS. The input file of this script is the output file of my DM script titled
 'batch_calc_t_over_lambda.s', which used DM's EELS module to batch calculate 
 t/lambda for a gob of low-loss spectra.
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
file_path = "C:/Dropbox/Crozier Group Users - Will Bowman/active_research/microscopy/150217_10Ca_XRDCrushed_ARM200kV/t_over_lambda_raw_DM_output.txt"
file_name_counter_prefix = "EELS_LL_" # to find file counter for sorting
file_name_counter_length = 2
data_string_prefix = "Relative sample thickness = " # to find t/lambda value
data_string_length = 4

''' ########################### FUNCTIONS ########################### '''
    
    
''' ########################### MAIN SCRIPT ########################### '''

lines = [ line.strip() for line in open( file_path ) ]

file_counters = []
file_names = []
t_over_lambdas = []

for line_string in lines:
    
    if line_string.__contains__( file_name_counter_prefix ):
        file_counter = wf.pluck_sub_string_counter( line_string, file_name_counter_prefix, file_name_counter_length )
        file_names.append( line_string )
        file_counters.append( file_counter )
        print( file_counter )
        
    elif line_string.__contains__( data_string_prefix ):
        t_over_lambda = wf.pluck_sub_string_counter( line_string, data_string_prefix, data_string_length )
        t_over_lambdas.append( t_over_lambda )
        print( t_over_lambda )
        
stacked_output = np.vstack( ( file_counters, file_names, t_over_lambdas ) ).T
    
''' ########################### REFERENCES ########################### '''