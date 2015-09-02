''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-08-28 by Will Bowman. This script plots composition from EELS for 
 boundaries vs. misorientation angle for the TEM OIM EELS manuscript
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
# path to data files for figure
data_dir = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_gb misorientation OIM EELS/figures/gpdc-concentration-misorientation-length-fraction/'
# name of composition vs misorientation angle data file
comp_v_misor_file = 'gpdc-gb-concentration-results_150828.txt'
# name of composition vs misorientation angle data file
# len_frac_v_misor_file = ''
# path to output directory
output_dir = data_dir
output_file = 'gpdc-concentration-misorientation-length-fraction'


x_label, y_label = 'Misorientation angle (Degrees)', 'Concentration (Mole fraction)'
x_min, x_max = 15, 65 # degrees
y_min, y_max = 0, 1 # mole fraction

dots, file_type = 300, 'png'


''' ########################### FUNCTIONS ########################### '''

def save_name( dir, name, dpi, file_type ):
    name = dir + name + '-' + str( dpi ) + 'dpi.' + file_type
    return name
    
''' ########################### MAIN SCRIPT ########################### '''

# read data (raw and background subtracted valence loss)
d = np.loadtxt( data_dir + comp_v_misor_file, skiprows = 1, delimiter = '\t' )
misor, gr_ce, gb_ce, d_ce, gr_pr, gb_pr, d_pr, gr_gd, gb_gd, d_gd = d.T

wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]

pl.close( 'all' )
pl.figure( figsize = ( 3.4, 3 ) )
ax = pl.gca()

pl.plot( misor, gr_ce, color = 'maroon', marker = 'D', mec = 'maroon', mfc = 'white', ls = '' )
pl.plot( misor, gb_ce, color = 'maroon', marker = 'D', mec = 'maroon', ls = '' )
pl.plot( misor, gb_gd, color = 'black', marker = 'o', mec = 'black', ls = '' )
pl.plot( misor, gr_gd, color = 'black', marker = 'o', mec = 'black', mfc = 'none', ls = '' )
pl.plot( misor, gb_pr, color = 'grey', marker = 's', mec = 'grey', ls = '' )
pl.plot( misor, gr_pr, color = 'grey', marker = 's', mec = 'grey', mfc = 'none', ls = '' )

entries = ( 'Ce', 'Ce GB', 'Gd GB', 'Gd', 'Pr GB', 'Pr' )
pl.legend( entries, loc = 'best', fontsize = fontsize, numpoints = 1, borderpad = 0.1, labelspacing = 0.1 )

pl.xlim( x_min, x_max )
pl.ylim( y_min, y_max )
pl.xlabel( x_label )
pl.ylabel( y_label )
# wf.centered_annotation( 0.45, 0.5 * y_max, 'ZLP', 'black', fontsize = fontsize )
# wf.centered_annotation( 2.6, 0.16 * y_max, 'Plateau', 'black', fontsize = fontsize )
pl.minorticks_on()
# ax.set_yticks([])
pl.tight_layout()


output_name = wf.save_name( data_dir, output_file, dots, file_type )
# pl.savefig( output_name, format = file_type, dpi = dots, transparent = True )
# pl.savefig( output_path_single_scattering + output_file_single_scattering + '-' + str( dots ) + 'dpi.png', format = 'png', dpi = dots )
    
''' ########################### REFERENCES ########################### '''