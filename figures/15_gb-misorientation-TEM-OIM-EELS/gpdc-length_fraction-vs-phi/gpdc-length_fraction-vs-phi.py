''' ########################### OVERVIEW ########################### '''
'''
 Created 2016-07-19 by Will Bowman. For plotting grain boundary length fraction
 vs. space charge potential computed from mebane code.
 
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
# absolute path to data

data_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Research_PhD/code/'+\
    'github/figures/15_gb-misorientation-TEM-OIM-EELS/'+\
    'gpdc-length_fraction-vs-phi/'
    
fig_dir = data_dir

# experimental misorientation angles (MAD)
d_ema = fig_dir + 'GPDC-FIB_misorientation-angles.txt'
d_ema_skiprows = 1
# misorientation angle distribution (MAD)
d_mad = fig_dir + 'GPDCfib_gbLengthFraction.txt'
d_mad_skiprows = 1
# mackenzian distribution
d_mack = fig_dir + 'mackenzie_200_bins-tdl.txt'
d_mack_skiprows = 7

# path to output directory
output_dir = data_dir
output_file = 'gpdc-length_fraction-vs-phi'
save = True
save = False
subfolder_save = True

# fig_size = ( 4, 3.4 ) # ( width, hight ) in inches
# subplot_white_space = 0.05 # see pl.subplots_adjust()
# # font size, resolution (DPI), file type
# fsize, dots, file_type = 10, [300], 'png'
# # wf.colors('col_name')
# cols = [ wf.colors('eth_blue'), 'black', 'grey', 'goldenrod' ]
# marks, msize = [ 's', 'o', '^', 'x' ], 6
# lines = [ '-', '' ]
# leg_ents = [ 'Layer', 'Interface', 'Reference' ]
# leg_loc = 'upper right'
# x_lab, y_lab = 'Energy loss (eV)', 'Counts (Arbitrary units)'
# x_lims, y_lims = [ [860,960], [1155,1240] ], [ [-1e4,15e4], [-1e4,15e4] ]
# x_maj_tick_loc = ['', 20]
# x_maj_tick_lab = [
#     [ '', '880', '900', '920', '940' ],
#     [ '', '', '1180', '', '1220' ]
#     ]
# file_anno = [''] # create multiple images each with an additional curve
# scale_x, scale_y = [], [7, 4, 0.6]
# shift_x, shift_y = [], [3e4, 1e3, -1700]
mack_scalar, mack_shift = 14, -0.004

# generate data objects from .txt, skip header rows, store cols as variables
# data = np.genfromtxt( d, skiprows=1, delimiter = '\t' )
ema, ema_stdev  = np.genfromtxt( d_ema, skiprows=d_ema_skiprows ).T
mad_ang, mad = np.loadtxt( d_mad, skiprows=d_mad_skiprows ).T
mack_ang, mack_cor, mack_rand = np.loadtxt( d_mack, skiprows=d_mack_skiprows ).T

mack = mack_rand * mack_scalar + mack_shift

na_gd = 0.0038 * mack_ang + 0.093
na_pr = 0.0021 * mack_ang + 0.036
na_pr3 = na_pr / 2 
na_gb3 = na_gd + na_pr3
na_ratio_3 = na_gb3 / 0.13
phi_gb = 0.6652 * na_ratio_3 - 0.622
# exp_phi_gb = 0.6652 * na_ratio_3 - 0.622

# m, b = np.polyfit( )
m_phi_gb_exp, b_phi_gb_exp = np.polyfit( mack_ang, phi_gb, 1 )
phi_gb_exp = m_phi_gb_exp * ema + b_phi_gb_exp

pl.close( 'all' )
pl.figure()
pl.plot( mack_ang, phi_gb, ls='-' )

t = phi_gb_exp
s = [ 7**2 for n in range( len( t ) ) ] # [2]
pl.scatter( ema, phi_gb_exp, s=s, c=phi_gb_exp, cmap=mpl.cm.spectral_r )
pl.colorbar()
pl.grid('on')
pl.legend( ['Phi vs. Misor. ang.'], loc='best' )

pl.figure()
pl.plot( phi_gb, mack, ls='-' )
pl.legend( ['Lenth fraction vs. Phi'], loc='best' )

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot( ema, phi_gb_exp, marker='s', ls='', cm= )
# plt.show()
# Axes3D.plot()


# # clipping data so no overflow in x-axis (svg rendering bug)
# eV_x_ce, lay_y_ce_clip, lims_x_ce = wf.clip_xy( x_lims[0], eV_x, lay_y )
# eV_x_gd, lay_y_gd_clip, lims_x_gd = wf.clip_xy( x_lims[1], eV_x, lay_y )
# eV_x_ce, int_y_ce_clip, lims_x_ce = wf.clip_xy( x_lims[0], eV_x, int_y )
# eV_x_gd, int_y_gd_clip, lims_x_gd = wf.clip_xy( x_lims[1], eV_x, int_y )

# # adjust data for plotting
# lay_y_pl_ce = lay_y_ce_clip + shift_y[0]
# lay_y_pl_gd = lay_y_gd_clip + shift_y[0]
# int_y_pl_ce = int_y_ce_clip
# int_y_pl_gd = int_y_gd_clip

# ''' ########################### FUNCTIONS ########################### '''

# def mpl_customizations():
#     wf.wills_mpl( fsize ) # pass the figure's fontsize
    
# def save_fig(output_file_name):
#     for dot in dots:
#         if subfolder_save:
#             output_dir = data_dir + wf.date_str() + '/'
#             if not os.path.isdir( output_dir ):
#                 os.mkdir( output_dir )
#         output_name = wf.save_name( output_dir, output_file_name, dot, file_type )
#         pl.savefig( output_name, format=file_type, dpi=dot, transparent=True )
#         pl.savefig( output_dir + output_file + '.svg', format = 'svg' )

# ''' ########################### MAIN SCRIPT ########################### '''

# for h in range( 1, len( file_anno ) + 1 ): # for plotting different dpis
  
#     pl.close( 'all' )
#     pl.figure( figsize = fig_size ) # ( width, height )
#     mpl_customizations() # apply customizations to matplotlib

#     # pl.subplot( 1, 2, 1 ) # subplot( height, width, subplot_number )
#     # gridspec( (rows,cols), (plot_location), colspan )
#     # pl.plot( ev_Ca, counts_Ca_off, color = col_off, dashes = dash )
#     pl.subplot2grid( (1,3), (0,0), colspan=2 )
#     pl.plot( eV_x_ce, lay_y_pl_ce, c=cols[0], ls=lines[0] )
#     pl.plot( eV_x_ce, int_y_pl_ce, c=cols[1], ls=lines[0] )

#     ax = pl.gca()
#     ax.set_ylabel( y_lab, labelpad=0 )
#     ax.set_xlabel( x_lab, labelpad=0, horizontalalignment='left' )
#     # ax.set_xlim( lims_x_ce[0], lims_x_ce[1] )
#     ax.set_xlim( lims_x_ce )
#     ax.set_ylim( y_lims[0][0], y_lims[0][1] )
#     ax.minorticks_on()
#     ax.set_xticklabels( x_maj_tick_lab[0] )
#     ax.set_yticklabels([])
#     # ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( Ca_major ) )

#     # LEGEND ON FIRST SUBPLOT
#     ax.legend( leg_ents, loc=leg_loc, handlelength=1.5, frameon=False, 
#         fontsize=fsize, labelspacing=.5, handletextpad=0.3, borderpad=0.1 )
#     pl.setp(ax.get_legend().get_lines(), linewidth=2) # the legend linewidth

#     # pl.subplot( 1, 2, 2 )
#     pl.subplot2grid( (1,3), (0,2) )
#     pl.plot( eV_x_gd, lay_y_pl_gd, c=cols[0], ls=lines[0] )
#     pl.plot( eV_x_gd, int_y_pl_gd, c=cols[1], ls=lines[0] )

#     ax = pl.gca()
#     # ax.set_xlim( lims_x_gd[0], lims_x_gd[1] )
#     ax.set_xlim( lims_x_gd )
#     ax.set_ylim( y_lims[1][0], y_lims[1][1] )

#     ax.minorticks_on()
#     ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( x_maj_tick_loc[1] ) )
#     ax.set_xticklabels( x_maj_tick_lab[1] )
#     ax.set_yticklabels([])

#     pl.subplots_adjust( wspace=subplot_white_space, bottom=0.15 )

#     # pl.tight_layout()
#     pl.show()
#     if save:
#         save_fig( output_file + file_anno[h-1] ) # save files at each dpi
'''
REFS
[1] http://stackoverflow.com/questions/17682216/scatter-plot-and-color-mapping-in-python
[2] http://stackoverflow.com/questions/14827650/pyplot-scatter-plot-marker-size
'''