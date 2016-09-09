''' ########################### OVERVIEW ########################### '''
'''
Created 2016-09-07 by Will Bowman.
This script generates a figure to illustrate core-loss EELS spectral 
quantification.
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import csv, imp, os
import wills_functions as wf
imp.reload(wf) # reload wf 
##

''' ########################### USER-DEFINED ########################### '''
# path to data file
paper_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/dissertation/'
fig_name = 'EELS-background-subtraction'
fig_dir = paper_dir + 'figures/' + fig_name + '/'
data_dir = paper_dir + 'data/' + fig_name + '/'

d_in = data_dir + '141007_2Ca_06.txt' # in data

leg_ents = [ 'Raw data' ]
leg_loc = 'best'
x_lab = [ 'Energy-loss (eV)' ]
y_lab = [ 'Intensity (Arbitrary units)' ]

# path to output directory
output_dir = fig_dir
output_file_name = fig_name
subfolder = True
save = True
# save = False

fig_size = ( 5, 3 ) # ( width, hight ) in inches

# font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']
cols = wf.cols()
dash, l_wid = [ 6, 1 ], 1 # [ pix_on pix_off ], linewidth
mark, msize, mwidth = wf.marks(), 7, 0.5

# naming sequence of figs with successive curves on same axis
file_anno = [ '-0of0' ] # for single fig with all curves
x_lims = [ 300, 1e3 ]
y_lims = [ 0, 10 ]
fill_xs = [
    [ [300, 340], [450, 520], [770, 875] ],
    [ [340, 390], [520, 580], [875, 950] ]
]
fill_cols =[ 'pink', wf.colors('pale_gold') ]


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize

def fill_windows( x, y0, y1, fill_xs, fill_c ):
    for i, xx in enumerate( fill_xs ):
        x_clipped, y_clipped, lims = wf.clip_xy( xx, x, y1 )
        pl.fill_between( x_clipped, y0, y_clipped, facecolor=fill_c, 
            edgecolor='grey' )
    
''' ########################### MAIN SCRIPT ########################### '''

# READ AND STORE DATA IN VARIABLES
d = np.genfromtxt( d_in, delimiter='\t' )

# store columns in variables
eV_d, I_d = d.T

# # clip raw data to x_lims to avoid .svg rendering issues
eV_p, I_p, x_lims_p = wf.clip_xy( x_lims, eV_d, I_d )

# # normalize, scale, shift curves for pretty plotting
I_p = I_p / np.nanmax( I_p ) * 10

''' ### GENERATE FIGURES ### '''
for i, anno in enumerate( file_anno ):
    
    pl.close( 'all' ) # close all open figures
    pl.figure( figsize=fig_size ) # create a figure ( w, h )
    mpl_customizations() # apply customizations to matplotlib

    pl.plot( eV_p, I_p, color=cols[0], lw=l_wid )
    # ( x, y0, y1, fill_xs, fill_c )
    fill_windows( eV_p, y_lims[0], I_p, fill_xs[0], bkgd_c )
    fill_windows( eV_p, y_lims[0], I_p, fill_xs[1], fill_c )
    
    ax0 = pl.gca() # store current axis
    ax0.set_xlim( x_lims_p )
    # ax0.set_ylim( y_lims[0] )
    ax0.set_xlabel( x_lab[0] )
    ax0.set_ylabel( y_lab[0] )
    # ax0.set_yticks([])
    # ax0.set_yticklabels([])
    ax0.minorticks_on()
    ax0.legend( leg_ents, loc=leg_loc, frameon=False, labelspacing=.1,
        handletextpad=.3, fancybox=False, borderpad=.3, fontsize=fsize,
        numpoints=1 )
    pl.tight_layout()


    pl.show()
    if save:
        wf.save_fig( output_dir, file_types, dots, output_file_name, anno='', 
            subfolder_save=subfolder )

''' ########################### REFERENCES ########################### '''
'''
1. 
'''