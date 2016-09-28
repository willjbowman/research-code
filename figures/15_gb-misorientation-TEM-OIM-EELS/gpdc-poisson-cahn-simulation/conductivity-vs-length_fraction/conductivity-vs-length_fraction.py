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
imp.reload(wf) # reload wf

##

''' ########################### USER-DEFINED ########################### '''
# absolute path to data
paper_dir =  'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/'+\
    '15_WJB_gb misorientation OIM EELS/'
sub_dir = ''
sub_dir = 'gpdc-poisson-cahn-simulation/'
fig_name = 'conductivity-vs-length_fraction'

fig_dir = paper_dir + 'figures/' + sub_dir + fig_name + '/'
data_dir = paper_dir + 'data/' + sub_dir + fig_name + '/'

# experimental misorientation angles from TSL
d_ema, d_ema_ski = data_dir + 'GPDC-FIB_misorientation-angles.txt', 1
# PGCO experimental misorientation angle distribution (MAD)
d_mad, d_mad_ski = data_dir + 'GPDCfib_gbLengthFraction.txt', 1
# mackenzian distribution
d_mack, d_mack_ski = data_dir + 'mackenzie_200_bins-tdl_no-head.txt', 0
    
# path to output directory
output_dir = fig_dir
output_file_name = fig_name + '_13-MolPer'
subfolder_save = True
save = True
save = False

fig_size = ( 3, 3 ) # ( width, hight ) in inches

# leg_ents = [ 'Layer', 'Interface', 'Reference' ]
# leg_loc = 'upper right'
x_labs = [
    [ 'Space charge potential (V)', 'Misor. ang. (Deg.)' ],
    [ r'log($\sigma_{GB}/\sigma_{Grain}$) @ 300 $^{\circ}\!$C',
        'Misor. ang. (Deg.)' ]
]
y_labs = [
    [ 'Length fraction', 'Sp. chg. pot. (V)' ],
    [ 'Length fraction', r'log($\sigma_{GB}/\sigma_{Grain}$)' ]
]
x_lims = [ [-.8,1.5], [1155,1240] ]
y_lims = [ [0,.3], [0,1.6] ]

# # font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']
cols = wf.cols()
marks, msize, mwidth = wf.marks(), 5, 0.5

''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize
    
''' ########################### MAIN SCRIPT ########################### '''

# READ AND STORE DATA IN VARIABLES #####

# misorientation angles measured during experiment
ema, ema_stdev  = np.genfromtxt( d_ema, skiprows=d_ema_ski ).T
# experimental PGCO MAD
mad_ang, mad = np.genfromtxt( d_mad, skiprows=d_mad_ski ).T
# mackenzian distribution generated using TSL
mack_ang, mack_cor, mack_rand = np.genfromtxt( d_mack, skiprows=d_mack_ski ).T


# MANIPULATE DATA #####

# scale and shift needed to fit mackenzian to experimental MAD
mack_scalar, mack_shift = 14, -0.004
mack = mack_rand * mack_scalar + mack_shift

# linear functions for gb cation concentration vs. misor. ang.
na_gd = 0.0038 * mack_ang + 0.093 # gd concentration
na_pr = 0.0021 * mack_ang + 0.036 # pr concentration
pr3_frac = 0.5 # assuming 50% are 3+

na_pr3 = na_pr * pr3_frac # pr3 concentration assuming 50% are 3+
na_3_gb = na_gd + na_pr3  # trivalent solute concentration
na_ratio_3 = na_3_gb / ( 0.11 + 0.04 * pr3_frac ) # na_gb / na_bulk

# lin. func. for phi vs. solute conc. at each misor. ang.
# 0% pr3+ : 0.4933, -0.4281
# phi_gb = 0.4933 * na_ratio_3 - 0.4281
# 50% pr3+ : 0.5801, -0.5273
phi_gb = 0.5801 * na_ratio_3 - 0.5273
# 100% pr3+ : 0.6652, -0.622
# phi_gb = 0.6652 * na_ratio_3 - 0.622

# m, b = np.polyfit( )
m_phi_gb_exp, b_phi_gb_exp = np.polyfit( mack_ang, phi_gb, 1 )
# predicted phis for misor angs in experiment
phi_gb_exp = m_phi_gb_exp * ema + b_phi_gb_exp

# polynomial function of log10( sig_gb/sig_gr ) vs. na

log10_sig_gb_gr = 20.71*na_3_gb - 23.19*na_3_gb - 13.78*na_3_gb + 2.31


# GENERATE FIGURES #####
mpl_customizations()
pl.close( 'all' )

# length fraction vs. space charge potential ##
pl.figure( figsize=fig_size ) # ( w, h ) inches

# pl.plot( phi_gb, mack, ls='-', c=wf.colors('dark_grey') )
pl.plot( phi_gb, mack, ls='-', c='maroon' )
ax0 = pl.gca()
ax0.set_xlabel( x_lab_0, labelpad=0.5 )
ax0.set_ylabel( y_lab_0, labelpad=0.5 )
ax0.set_xlim( x_lims[0] )
ax0.set_ylim( y_lims[0] )
ax0.minorticks_on()
pl.tight_layout()

ax1 = pl.axes([ .35, .55, .3, .3 ]) # [ L, B, W, H ] relative to figure

# pl.figure()
# pl.plot( mack_ang, phi_gb, ls='-' )
t = phi_gb_exp
s = [ 7**2 for n in range( len( t ) ) ] # [2]
pl.scatter( ema, phi_gb_exp, s=s, c=phi_gb_exp, cmap=mpl.cm.spectral_r )
# pl.colorbar()
ax1.set_xlabel( x_lab_1, labelpad=0.5 )
ax1.set_ylabel( y_lab_1, labelpad=0.5 )
ax1.xaxis.set_major_locator( mpl.ticker.MultipleLocator( 20 ) )
ax1.yaxis.set_major_locator( mpl.ticker.MultipleLocator( .4 ) )
# ax1.set_xlim( x_lims[1] )
ax1.set_ylim( y_lims[1] )
ax1.minorticks_on()

if save:
    save_fig( output_file )

pl.figure( figsize=fig_size ) # ( w, h ) inches
# pl.plot( mack_ang, phi_gb, ls='-' )
t = phi_gb_exp
s = [ 7**2 for n in range( len( t ) ) ] # [2]
pl.scatter( ema, phi_gb_exp, s=s, c=phi_gb_exp, cmap=mpl.cm.spectral_r )
pl.colorbar()
pl.tight_layout()

if save:
    save_fig( output_file + '_colorbar' )


# length fraction vs. sig_gb/sig_gr ##
pl.figure( figsize=(3.5,3) ) # ( w, h ) inches

# pl.plot( log10_sig_gb_gr, mack, ls='-', c='maroon' )
t = log10_sig_gb_gr
s = [ 7**1.5 for n in range( len( t ) ) ] # [2]
pl.scatter( t, mack, s=s, c=t, cmap=mpl.cm.spectral, edgecolors='none' )
pl.colorbar()

ax0 = pl.gca()
ax0.set_ylabel( y_labs[1][0], labelpad=0.5 )
ax0.set_xlabel( x_labs[1][0], labelpad=0.5 )
# ax0.set_xlim( x_lims[0] )
ax0.set_ylim( y_lims[0] )
ax0.minorticks_on()
pl.tight_layout()

# ax1 = pl.axes([ .32, .55, .3, .3 ]) # [ L, B, W, H ] relative to figure

# t = log10_sig_gb_gr
# s = [ 7**2 for n in range( len( t ) ) ] # [2]
# pl.scatter( ema, log10_sig_gb_gr, s=s, c=phi_gb_exp, cmap=mpl.cm.spectral_r )
# # pl.colorbar()
# ax1.set_ylabel( y_labs[1][1], labelpad=0.5 )
# ax1.set_xlabel( x_labs[1][1], labelpad=0.5 )
# ax1.yaxis.set_major_locator( mpl.ticker.MultipleLocator( .4 ) )
# ax1.xaxis.set_major_locator( mpl.ticker.MultipleLocator( 20 ) )
# # ax1.set_xlim( x_lims[1] )
# # ax1.set_ylim( y_lims[1] )
# ax1.minorticks_on()

if save:
    save_fig( output_file )

# pl.figure( figsize=( 3.5, 3 ) ) # ( w, h ) inches
# # pl.plot( mack_ang, phi_gb, ls='-' )
# pl.tight_layout()

# if save:
#     save_fig( output_file + '_colorbar' )

'''
REFS
[1] http://stackoverflow.com/questions/17682216/scatter-plot-and-color-mapping-in-python
[2] http://stackoverflow.com/questions/14827650/pyplot-scatter-plot-marker-size
'''