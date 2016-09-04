''' ########################### OVERVIEW ########################### '''
'''
Created 2016-09-01 by Will Bowman.
This script is for plotting zlp/low-loss pattern of 10PCO PLD pellet for a figure
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
paper_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/' +\
    '16_PCO-gb-valence-mapping/'
fig_name = 'PCO-HRTEM'
fig_dir = paper_dir + 'figures/' + fig_name + '/'
data_dir = paper_dir + 'data/' + fig_name + '/'
d_in = data_dir + 'XRD-10PCO-pellet-CeO2-ref.txt'
# ref_d0 =  data_dir + 'CaO_Fm-3m_225_Shen_2001_MatResBull_20275.csv'
# ref_d1 =  data_dir + 'CaO2_F4--mmm_139_Kotov_1941_ZhurFizichKhim_20275.csv'

# path to output directory
output_dir = fig_dir
output_file = fig_name
subfolder_save = True
save = True
# save = False

fig_size = ( 3, 3 ) # ( width, hight ) in inches

# font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']
cols = [ 'maroon', 'grey', 'black', 'goldenrod' ]
dash, width = [ 6, 1 ], 1 # [ pix_on pix_off ], linewidth
norm = 100
# marks, msize, mwidth = [ 's', 'o' ], 7, 0.5
leg_ents = [ '10PCO pellet', r'$CeO{_2}$ ref.' ]
leg_loc = 'upper right'
x_lab = '${2\Theta}$ (Degrees)'
y0_lab, y1_lab = 'Counts (Arbitrary units)', ''
# naming sequence of figs with successive curves on same axis
# file_anno = [ '-0of1', '-1of1' ]
file_anno = [ '-0of0' ] # for single fig with all curves
x_lims, y0_lims, y1_lims = [25, 60], [-1.1, 1.1], [.1, .6]
y_shift_pco, y_shift_ceo2 = 0, -1
# y1_ticks = False


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize
    
    
''' ########################### MAIN SCRIPT ########################### '''

# READ AND STORE DATA IN VARIABLES
# d = np.loadtxt( data, skiprows = 1 )
d = np.genfromtxt( d_in, skiprows=2, delimiter='\t' )
# d_ref0 = np.genfromtxt( ref_d0, delimiter = ',' )

# store columns in variables
d_x_ceo2, d_y_ceo2, zz, d_x_pco, d_y_pco = d.T

# clip raw data to x_lims to avoid .svg rendering issues
x_pco, y_pco, x_lims_pco = wf.clip_xy( x_lims, d_x_pco, d_y_pco )
x_ceo2, y_ceo2, x_lims_ceo2 = wf.clip_xy( x_lims, d_x_ceo2, d_y_ceo2 )

# normalize, scale, shift curves for pretty plotting
y_pco_p = y_pco / np.nanmax( y_pco ) + y_shift_pco
y_ceo2_p = y_ceo2 / np.nanmax( y_ceo2 ) + y_shift_ceo2

''' ### GENERATE FIGURES ### '''
for i, anno in enumerate( file_anno ):
# if len( file_anno ) == 0:
    
    pl.close( 'all' ) # close all open figures
    pl.figure( figsize=fig_size ) # create a figure ( w, h )
    mpl_customizations() # apply customizations to matplotlib
    fontsize = mpl.rcParams[ 'font.size' ]

    # pl.subplot2grid( (1,2), (0,0) ) # ((rows,cols),(subplot_index))
    
    pl.plot( x_pco, y_pco_p, color=cols[0], lw=width )
    pl.plot( x_ceo2, y_ceo2_p, color=cols[1], lw=width, dashes=dash )
    
    ax0 = pl.gca() # store current axis
    ax0.set_xlim( x_lims_pco )
    ax0.set_ylim( y0_lims )
    ax0.set_xlabel( x_lab )
    ax0.set_ylabel( y0_lab )
    ax0.set_yticks([])
    ax0.minorticks_on()
    ax0.legend( leg_ents, loc=leg_loc, frameon=False, labelspacing=.1,
        handletextpad=.1 )

    # pl.subplot2grid( (1,2), (0,1) ) # ((rows,cols),(subplot_index))
    
    # # pl.plot( x_2p, norm_ys[0], color=cols[0], lw=width )
    # # pl.plot( x_2s, norm_ys[1], color=cols[0], lw=width, dashes=dash )
    
    # ax1 = pl.gca() # store current axis
    # ax1.set_xlim( x_lims_1 )
    # ax1.set_ylim( y1_lims_1 )
    # ax1.set_xlabel( x_lab )
    # ax1.set_ylabel( y1_lab )
    # ax1.set_yticks([])
    # ax1.minorticks_on()
    
    # ax1_leg_hand = mpl.lines.Line2D( [], [], c=cols[0], marker=marks[0],
        # ms=msize, ls='' )    
    # ax1.legend( [ax1_leg_hand], leg_ents, loc = 'upper right',
    #     numpoints =  1, frameon = False, fontsize = 10, labelspacing = .01,
    #     handletextpad = .01 )
    #         
    pl.tight_layout() # can run once to apply to all subplots, i think
    pl.show()
    if save:
        wf.save_fig( fig_dir, file_types, dots, output_file, anno )

''' ########################### REFERENCES ########################### '''
'''
1. 
'''