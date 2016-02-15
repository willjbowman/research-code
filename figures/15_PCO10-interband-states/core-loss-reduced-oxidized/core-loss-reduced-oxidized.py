''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-06-22 by Will Bowman. This script plots core-loss data for 
 the PCO manuscript.
 The oxidized spectrum was stretched and shifted such that the 4+ M54 peaks 
 overlay.
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
# path to data file
reduced_data_path = 'C:/Crozier_Lab/Writing/2015_PCO10 interband states/data/pco-m-reduced.txt'
oxidized_data_path = 'C:/Crozier_Lab/Writing/2015_PCO10 interband states/data/pco-m-oxidized.txt'

x_min, x_max = 870, 960 # eV
y_min, y_max = -200, 6e3 # eV
x_shift, y_shift = -56.51, 1e3 # eV, counts
x_stretch = 19.041 / 17.861
x_label, y_label = 'Energy-loss (eV)', 'Counts (Arbitrary units)'

output_file_path = 'C:/Crozier_Lab/Writing/2015_PCO10 interband states/figures/core-loss-reduced-oxidized/'
output_file_name = 'core-loss-reduced-oxidized'


''' ########################### FUNCTIONS ########################### '''
    
    
''' ########################### MAIN SCRIPT ########################### '''
# read data (reduced and oxidized spectra)
reduced_data = np.loadtxt( reduced_data_path )
oxidized_data = np.loadtxt( oxidized_data_path )
ev_reduced, raw_reduced, processed_reduced = reduced_data.T
ev_oxidized, raw_oxidized, processed_oxidized = oxidized_data.T
reduced_norm, oxidized_norm = wf.normalize_to_max( processed_reduced, processed_oxidized )

pl.close( 'all' )

wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]

pl.figure( figsize = ( 7, 3 ) )
ax = pl.gca()

pl.plot( ev_reduced, reduced_norm + y_shift, color = 'maroon', lw = 0.8, dashes = [ 2, 2 ] )
pl.plot( ev_oxidized * x_stretch + x_shift, oxidized_norm, color = 'maroon', lw = 0.8, ls = '-' )
pl.legend( ( 'Reduced', 'Oxidized' ), loc = 'upper right', fontsize = fontsize )

pl.xlim( x_min, x_max )
pl.ylim( y_min, y_max )
pl.xlabel( x_label )
pl.ylabel( y_label )

# wf.centered_annotation( 0.45, 0.5 * y_max, 'ZLP', 'black', fontsize = fontsize )
# wf.centered_annotation( 2.6, 0.16 * y_max, 'Plateau', 'black', fontsize = fontsize )

pl.minorticks_on()
ax.set_yticks([])
pl.tight_layout()

# pl.savefig( output_file_path + output_file_name + '.png', format = 'png', dpi = 1000 )
# pl.savefig( output_file_path + output_file_name + '.pdf', format = 'pdf', dpi = 1000 )

    
''' ########################### REFERENCES ########################### '''