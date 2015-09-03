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
# path to data file (make gui to pick files?)
data_dir = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/...'

# 
eels_d = data_dir + 'eels-data/140203_3aGPDCfib_EELSSI2_highloss_gbAB.txt'

# path to output directory
output_dir = data_dir
output_file = 'gpdc-concentration'

# font size, resolution (DPI), file type
fsize, dots, file_type = 10, [300,1200], 'png'

# example plot info
eels_x_lab, eels_y_lab = 'Energy loss (eV)', 'Counts\n(Arb. units)'
eels_entries = ( 'Grain', 'G.B.' )
eels_x, eels_y = [ 860, 1250 ], [ -1e3, None ]
c_eels, ls_on = 'maroon', (4,1)
percent_shift = 200
eels_x_maj_loc = 100


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations(): # add custom styling unique to this figure
    wf.wills_mpl()
    mpl.rc( 'font', family='sans-serif', serif='Helvetica', weight='normal',size=fsize )
    mpl.rc( 'lines', linewidth=1.0, mew=0.01, markersize=3 )
    mpl.rc( 'legend', borderpad = 0.1, labelspacing = 0.1 )

# this method is helpful for multi-plot figures with similar styling
def eels_style( ax ):
    pl.xlim( eels_x )
    pl.ylim( eels_y )
    pl.minorticks_on()
    ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( eels_x_maj_loc ) )
    ax.yaxis.set_ticklabels([]) # y tick labels off    
    

''' ########################### MAIN SCRIPT ########################### '''

# read data, skip header rows
d_ev, d_off, d_on = np.loadtxt( eels_d, skiprows = 2 ).T

pl.close( 'all' ) # close all open figures
pl.figure( figsize = ( 3.4, 3 ) ) # create a figure of size ( width", height" )
ax = pl.gca() # store current axis

wf.mpl_customizations() # apply mpl customizations for this figure
# wf.slide_art_styles() # figure styling

# example of subplot
pl.subplot( 2, 3, 1 ) # ( sub_y, sub_x, sub_i )
ax1 = pl.gca()
pl.plot( d_ev, stack( d_off, d_on ), c=c_eels )
pl.plot( d_ev, d_on, c=c_eels, dashes=ls_on )
eels_style( ax1 )
pl.ylabel( eels_y_lab, labelpad=0.5 )
pl.legend( eels_entries, loc='upper center', fontsize=fsize )

# applies to subplots, pad in min pad on subplots, h_pad defined vertical spacing
pl.tight_layout( pad=0.3, h_pad=0.6 )

for dot in dots: # save a file for each resolution in dots
    output_name = wf.save_name( data_dir, output_file, dot, file_type )
    pl.savefig( output_name, format = file_type, dpi = dot, transparent = True )
    
''' ########################### REFERENCES ########################### '''