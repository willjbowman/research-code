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
data_dir = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_gb misorientation OIM EELS/figures/gpdc-misorientation-angle-distribution'
data_file_name = '/GPDCfib_gbLengthFraction.txt'
mackenzian_file_name = '/mackenzie_200_bins-tdl.txt'

mack_scalar, mack_shift = 14, -.004

x_min, x_max = 0, 4.9 # eV
y_min, y_max = 0, 7e2 # eV
x_label, y_label = 'Misorientation angle (degrees)', 'Length fraction'

output_dir = data_dir
output_file_name = '/gpdc-misorientation-angle-distribution-v1'
dots = 300


''' ########################### FUNCTIONS ########################### '''
    
    
''' ########################### MAIN SCRIPT ########################### '''
# read and store data (orientation angle distribution and mackenzian)
d_mad = np.loadtxt( data_dir + data_file_name )
d_mack = np.loadtxt( data_dir + mackenzian_file_name, skiprows = 7 )
angle_mad, mad = d_mad.T
angle_mack, mack_correlated, mack_number = d_mack.T

pl.close( 'all' )

wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]

fig_width = wf.mm2in( 84 ) # 3.307 in
pl.figure( figsize = ( 3.0, 1.9 ) ) # ( width, height )
ax = pl.gca()

mack_plot = mack_number * mack_scalar + mack_shift
pl.plot( angle_mack, mack_plot, color = 'grey', linewidth = 1, linestyle = '-' )
pl.plot( angle_mad, mad, color = 'maroon', marker = 'o', linestyle = '' )

pl.legend( ( 'Mackenzie \n(random)', 'GPDC' ), loc = 'upper left', 
    numpoints = 1, frameon = False, fontsize = fontsize )

# pl.xlim( x_min, x_max )
# pl.ylim( y_min, y_max )
pl.xlabel( x_label )
pl.ylabel( y_label )
# wf.centered_annotation( 0.45, 0.5 * y_max, 'ZLP', 'black', fontsize = fontsize )
# wf.centered_annotation( 2.6, 0.16 * y_max, 'Plateau', 'black', fontsize = fontsize )
pl.minorticks_on()
ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( 5e-2 ) )
# ax.set_yticks([])
pl.tight_layout()


pl.savefig( output_dir + output_file_name + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots, transparent = True )
# pl.savefig( output_file_path + output_file_name + '.pdf', format = 'pdf', dpi = 1000 )

    
''' ########################### REFERENCES ########################### '''