''' ########################### OVERVIEW ########################### '''
'''
 Created 2016-12-06 by Will Bowman. For plotting multiple EELS edges to compare
 different spectra.
 
 This script will save a figure with the script's file name to a subfolder
 whose name is the current date yyyymmdd
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
# path to data

paper_dir = 'C:/Users/Besitzer/Dropbox/WillB/ETH/writing/'+\
    '16_Schweiger S etal_Symmetric memristor/'
fig_name = 'interface-EELS'
fig_dir = paper_dir + 'figs/' + fig_name + '/'
data_dir = paper_dir + 'data/' + fig_name + '/'

# single file with both spectra as columns
d_ce_in = data_dir +\
    '160716_ERO-GDC-x3_EELS-SI_07_S_c2_eels-CL_700meV_3mm--SI_signal_Ce.txt'
d_ce_in_r = 0
d_gd_in = data_dir +\
    '160716_ERO-GDC-x3_EELS-SI_07_S_c2_eels-CL_700meV_3mm--SI_signal_Gd.txt'
d_gd_in_r = 0

# path to output directory
output_dir = fig_dir # save output figs with the data
output_file_name = fig_name
subfolder = True
save = True
# save = False

fig_size = ( 4.5, 3.4 ) # ( width, hight ) in inches

# font size, resolution (DPI), file type
leg_ents = [ '7.8 nm', '5.2 nm', '2.6 nm', '0 nm' ]
leg_loc = 'upper right'
x_labs = [ 'Energy-loss (eV)', 'Energy-loss (eV)' ]
y_labs = [ 'Counts (Arb. units)', '' ]
x_lims = [ [860,940], [1150,1260] ]
y_lims = [ [-1.6,1.1], [-1.7,1.1] ]

fsize, dots, file_types = 10, [300], ['png','svg']
# cols = wf.cols()
cols = [ wf.colors('eth_blue'), wf.colors('eth_green'), 'goldenrod', 'maroon' ]
marks, msize, mwidth = wf.marks(), 5, 0.5
lwidth = 2

x_maj_tick_loc = ['', 20]
x_maj_tick_lab = [
    [ '', '880', '900', '920', '940' ],
    [ '', '1160', '', '1200', '', '1240' ]
]

spectra_span = [ [0,6], [18,24], [35,41], [70,76] ]
ev_0_ce, ev_0_gd, dispersion = 768.2, 1033.5, .7 # eV
y_shift = 0.5
file_anno = ''

''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize

''' ########################### MAIN SCRIPT ########################### '''

# generate data objects from .txt
d_ce = np.genfromtxt( d_ce_in, skiprows=d_ce_in_r, delimiter='\t' )
d_gd = np.genfromtxt( d_gd_in, skiprows=d_gd_in_r, delimiter='\t' )

chans_ce = np.size( d_ce, 1 )
d_ev_ce = np.linspace( 0, chans_ce, chans_ce ) * dispersion
d_ev_ce = d_ev_ce + ev_0_ce
chans_gd = np.size( d_gd, 1 )
d_ev_gd = np.linspace( 0, chans_gd, chans_gd ) * dispersion
d_ev_gd = d_ev_gd + ev_0_gd

pl.close( 'all' )
pl.figure( figsize=fig_size ) # ( width, height )
mpl_customizations() # apply customizations to matplotlib

# ((rows,cols),(subplot_index),rowspan=)
pl_ce = pl.subplot2grid( (1,3), (0,0), colspan=2 )
ax_ce = pl_ce.axes
pl_gd = pl.subplot2grid( (1,3), (0,2) )
ax_gd = pl_gd.axes

for i, span in enumerate( spectra_span ):
    
    ce_spectra_sum = wf.normalize( d_ce[ span[0]:span[1] ].sum( axis=0 ), 1 )

    # clipping data so no overflow in x-axis (svg rendering bug)
    # eV_ce, I_clip_ce, lims_x_ce = wf.clip_xy( x_lims[0], eV_x, lay_y )

    ax_ce.plot( d_ev_ce, ce_spectra_sum - i * y_shift, c=cols[i], 
        linewidth=lwidth )
    # pl.plot( eV_x_ce, int_y_pl_ce, c=cols[1], ls=lines[0] )

    ax_ce.set_ylabel( y_labs[0] )
    ax_ce.set_xlabel( x_labs[0] )
    # ax.set_xlabel( x_lab, labelpad=0, horizontalalignment='left' )
    # # ax.set_xlim( lims_x_ce[0], lims_x_ce[1] )
    ax_ce.set_xlim( x_lims[0] )
    ax_ce.set_ylim( y_lims[0] )
    ax_ce.minorticks_on()
    # ax.set_xticklabels( x_maj_tick_lab[0] )
    ax_ce.set_yticklabels([])

for i, span in enumerate( spectra_span ):

    gd_spectra_sum = wf.normalize( d_gd[ span[0]:span[1] ].sum( axis=0 )[0:500], 1 )
    ax_gd.plot( d_ev_gd[0:500], gd_spectra_sum - i * y_shift, c=cols[i], 
        linewidth=lwidth )

    ax_gd.set_ylabel( y_labs[1] )
    ax_gd.set_xlabel( x_labs[1] )
    # ax.set_xlabel( x_lab, labelpad=0, horizontalalignment='left' )
    # # ax.set_xlim( lims_x_gd[1], lims_x_gd[1] )
    ax_gd.set_xlim( x_lims[1] )
    ax_gd.set_ylim( y_lims[1] )
    ax_gd.minorticks_on()
    ax_gd.set_xticklabels( x_maj_tick_lab[1] )
    ax_gd.set_yticklabels([])

pl.subplots_adjust( wspace=subplot_white_space, bottom=0.15 )

pl.tight_layout()
if save:
    wf.save_fig( output_dir, file_types, dots, output_file_name, anno=file_anno,
        subfolder_save=subfolder )