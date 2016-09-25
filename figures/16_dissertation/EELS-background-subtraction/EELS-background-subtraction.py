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

d_in = data_dir + fig_name + '.txt' # in data

leg_ents = [ 'Raw data', r'Background fit $(I=AE\/^{-r})$', 
    'Bkgd.-subtracted signal', 'Bkgd. fitting window', 'Integrated signal' ]
leg_loc = 'best'
x_lab = [ 'Energy-loss (eV)' ]
y_lab = [ 'Intensity (Arbitrary units)' ]

# path to output directory
output_dir = fig_dir
output_file_name = fig_name
subfolder = True
save = True
save = False

fig_size = ( 5, 3 ) # ( width, hight ) in inches

# font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']
cols = wf.cols()
dash, l_wid = [ [], [3,3], [3,1] ], 1 # [ pix_on pix_off ], linewidth
mark, msize, mwidth = wf.marks(), 7, 0.5
line = [ '-', '--', ]

# naming sequence of figs with successive curves on same axis
file_anno = [ '-0of0' ] # for single fig with all curves
x_lims = [ 300, 1e3 ]
y_lims = [ 0, 10 ]
y_tic_lab = [ np.arange(0,10,1) ]
fill_xs = [
    [ [300, 340], [450, 520], [770, 875] ], 
    [ [340, 390], [520, 580], [875, 950] ]
]
norm_max = 10
fill_col =[ ['pink', wf.colors('pinker') ], 
    [ wf.colors('pale_gold'), 'goldenrod'] ] # [bkgd,border], [signal,border]


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize

# y0 can be constant or function
def fill_windows( x, y0, y1, fill_xs, fill_c, fill_lab ):

    for i, xx in enumerate( fill_xs ):
        y0_clipped = y0
        if type( y0 ) is np.ndarray: # if y_bot is a curve
            x_clipped, y0_clipped, lims = wf.clip_xy( xx, x, y0 )
        x_clipped, y1_clipped, lims = wf.clip_xy( xx, x, y1 )
        pl.fill_between( x_clipped, y0_clipped, y1_clipped, facecolor=fill_c[0], 
            edgecolor=fill_c[1], label=fill_lab )

# from matplotlib.patches import Rectangle

# p1 = Rectangle((0, 0), 1, 1, fc="green")
# p2 = Rectangle((0, 0), 1, 1, fc="red")
# legend([p1, p2], [a1_label, a2_label])
    
''' ########################### MAIN SCRIPT ########################### '''

# READ AND STORE DATA IN VARIABLES
d = np.genfromtxt( d_in, delimiter='\t' )

# store columns in variables
eV_d, raw_d, bkgd_d, sig_d, xsec_d = d.T

# # clip data to x_lims to avoid .svg rendering issues
# REFACTOR!
eV_p, raw_p, x_lims_p = wf.clip_xy( x_lims, eV_d, raw_d )
eV_p, bkgd_p, x_lims_p = wf.clip_xy( x_lims, eV_d, bkgd_d )
eV_p, sig_p, x_lims_p = wf.clip_xy( x_lims, eV_d, sig_d )

# normalize, scale, shift curves for pretty plotting
# raw_p = wf.normalize( raw_p, norm_max )
# bkgd_p = wf.normalize( bkgd_p, norm_max )
# sig_p = wf.normalize( sig_p, norm_max )

''' ### GENERATE FIGURES ### '''
for i, anno in enumerate( file_anno ):
    
    pl.close( 'all' ) # close all open figures
    pl.figure( figsize=fig_size ) # create a figure ( w, h )
    mpl_customizations() # apply customizations to matplotlib

    p0, = pl.plot( eV_p, raw_p, color=cols[0], lw=l_wid, label=leg_ents[0] )
    p1, = pl.plot( eV_p, bkgd_p, color=cols[1], lw=l_wid, label=leg_ents[1], 
        dashes=dash[1] )
    p2, = pl.plot( eV_p, sig_p, color=cols[2], lw=l_wid, label=leg_ents[2], 
        dashes=dash[2] )

    # ( x, y0, y1, fill_xs, fill_col )
    # background
    fill_windows( eV_p, y_lims[0], raw_p, fill_xs[0], fill_col[0], fill_lab[0] )
    p3 = mpl.patches.Rectangle( (0,0), 1, 1, fc=fill_col[0][0], ec=fill_col[0][1] )
    # signals
    fill_windows( eV_p, bkgd_p, raw_p, fill_xs[1], fill_col[1], fill_lab[1] )
    fill_windows( eV_p, y_lims[0], sig_p, fill_xs[1], fill_col[1], fill_lab[1] )
    p4 = mpl.patches.Rectangle( (0,0), 1, 1, fc=fill_col[1][0], ec=fill_col[1][1] )
    
    ax0 = pl.gca() # store current axis
    ax0.set_xlim( x_lims_p )
    ax0.set_ylim( y_lims[0] )
    ax0.set_xlabel( x_lab[0] )
    ax0.set_ylabel( y_lab[0] )
    # ax0.set_yticks([])
    ax0.set_yticklabels( y_tic_lab[0] )
    ax0.minorticks_on()
    ax0.legend( [p0,p1,p2,p3,p4],leg_ents, loc=leg_loc, frameon=False, 
        labelspacing=.1, handletextpad=.3, fancybox=False, borderpad=.3, 
        fontsize=fsize, numpoints=1 )
    
    pl.tight_layout()

    pl.show()
    if save:
        wf.save_fig( output_dir, file_types, dots, output_file_name, anno='', 
            subfolder_save=subfolder )

''' ########################### REFERENCES ########################### '''
'''
1. 
'''