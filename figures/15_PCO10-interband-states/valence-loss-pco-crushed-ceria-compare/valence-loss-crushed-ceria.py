''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-06-22 by Will Bowman. This script plots valence-loss data for 
 the PCO manuscript
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
data_dir = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_PCO10 interband states/figures/valence-loss-crushed-ceria'
data_file_name = '/140207_7bCeO2crush_Nion_EELS10_100kV_Ref20i_slit_1mm_5meV_25meV_5s_1frame.txt'

x_min, x_max = 0, 4.9 # eV
y_min, y_max = 0, 7e2 # eV
x_label, y_label = 'Energy-loss (eV)', 'Counts (Arbitrary units)'

output_dir = data_dir
output_file_name = 'valence-loss-crushed-ceria'


''' ########################### FUNCTIONS ########################### '''
    
    
''' ########################### MAIN SCRIPT ########################### '''
# read data (raw and background subtracted valence loss)
data = np.loadtxt( data_dir + data_file_name )
ev, data = data.T

pl.close( 'all' )

wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]

pl.figure( figsize = ( 3.4, 3 ) )
ax = pl.gca()

pl.plot( ev, data, color = 'maroon', lw = 0.5, ls = '-' )
# pl.legend( ( 'Raw', 'Processed' ), loc = 'upper left', fontsize = fontsize )
pl.xlim( x_min, x_max )
pl.ylim( y_min, y_max )
pl.xlabel( x_label )
pl.ylabel( y_label )
wf.centered_annotation( 0.45, 0.5 * y_max, 'ZLP', 'black', fontsize = fontsize )
# wf.centered_annotation( 2.6, 0.16 * y_max, 'Plateau', 'black', fontsize = fontsize )
pl.minorticks_on()
ax.set_yticks([])
pl.tight_layout()

# pl.savefig( output_file_path + output_file_name + '.png', format = 'png', dpi = 1000 )
# pl.savefig( output_file_path + output_file_name + '.pdf', format = 'pdf', dpi = 1000 )

    
''' ########################### REFERENCES ########################### '''