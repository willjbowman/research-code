''' ########################### OVERVIEW ########################### '''
'''
 Created xxxx-xx-xx by Will Bowman. This ...
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
# make gui to pick files?
data_dir = '' # path to data file

# path to output directory
output_dir = data_dir
output_file = 'gpdc-concentration-misorientation-length-fraction'

dots, file_type = 300, 'png' # output file resolution (DPI), file type

''' ########################### FUNCTIONS ########################### '''
    
    
''' ########################### MAIN SCRIPT ########################### '''
_data = np.loadtxt( _data_path, skiprows = 3 ) # read data, ignore first three rows

pl.close( 'all' ) # close all open figures
pl.figure( figsize = ( 3.4, 3 ) ) # create a figure
ax = pl.gca() # store current axis

wf.mpl_customizations() # apply customizations to matplotlib
wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]


pl.tight_layout() # can run once to apply to all subplots, i think

output_name = wf.save_name( data_dir, output_file, dots, file_type )
pl.savefig( output_name, format = file_type, dpi = dots, transparent = True )
    
''' ########################### REFERENCES ########################### '''