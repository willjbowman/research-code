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
sub_dir = 'gpdc-poisson-cahn-simulation/' # comment if no subdir
fig_name = 'conductivity-vs-length_fraction'
name_ext = [ '_Space-charge-dist', 
             '_Space-charge-dist_cmap', 
             '_Trival-conc-gb-dist', 
             '_Ea-gb-dist',
             '_Conductiv-dist' ]

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
output_file_name = fig_name + '_13-MolePer'
subfolder = True
save = True
# save = False # comment out for saving

fig_size = ( 3, 3 ) # ( width, hight ) in inches

# leg_ents = [ 'Layer', 'Interface', 'Reference' ]
# leg_loc = 'upper right'

labs = [ # [x,y]
    [ 
       [ 'Space charge potential (V)', 'Length fraction' ],
       [ 'Misor. ang. (Deg.)', 'Sp. chg. pot. (V)' ]
    ],
    [ 'Misorientation angle (Deg.)', 'Space charge potential (V)' ],
    [ r'$[A^{3+}]_{GB}$ (Mole%)', 'Length fraction' ],
    [ r'$E_a^{GB}$ (eV)', 'Length fraction' ],
    [ r'log($\sigma_{GB}/\sigma_{Grain}$)', 'Length fraction' ]
]

lims = [ # [x,y]
    [ 
       [ [0,.3], [-.8,1] ],
       [ [], [] ],
    ],
    [ [], [] ],
    [ [], [] ],
    [ 
        [ [0,.3],[] ], 
        [ [.9,1.15],[0,.2] ] # inset
    ],
    [ 
        [ [0,.3],[] ],
        [ [-4,-1.5],[0,.2] ] # inset
    ]
]

x_lims = [ [-.8,1], [1155,1240] ]
y_lims = [ [0,.3], [0,1] ]

# fit of Ea vs. [solute]
# P_ea = [ -10, 7.7143, 0.1714, 0.634 ] # from Ea_grain lit
P_ea = [ -78.456, 103.9, -43.82, 6.8439 ] # from Ea_GBs Gd-only
P_ea = [ -47.831, 64.583, -28.225, 5.0159 ] # from Ea_GBs all

# outputs of MatLab simulation script
# P_phi = [ 1.4599, -2.5358, 3.9246, -0.4624 ] # 'P_phi_vs_na_gb' in .m; 0 Pr3+
P_phi = [ 1.4599, -2.5358, 3.9246, -0.4624 ] # 'P_phi_vs_na_gb' in .m; 0.5 Pr3+
# P_phi = [ 1.4599, -2.5358, 3.9246, -0.4624 ] # 'P_phi_vs_na_gb' in .m; 1 Pr3+
P_cond = [ 87.1720, -65.6588, -3.5286, 1.5086 ]
P_cond = [ 689.6156, -912.1475, 383.6245, -53.1429 ] # Ea_Gr = 0.78 eV
# P_cond = [ 689.6156, -912.1475, 383.6245, -53.8470 ] # Ea_Gr = 0.7 eV
P_cond = [ 420.0889, -566.1236, 246.3749, -37.0549 ] # Ea_Gr=0.78, Ea_GB all data

# # font size, resolution (DPI), file type
fsize, dots, file_types = 10, [300], ['png','svg']
cols = wf.cols()
marks, msize, mwidth = wf.marks(), 5, 0.5
cmaps = [
    mpl.cm.spectral_r, mpl.cm.spectral_r, mpl.cm.spectral_r, mpl.cm.cool_r,
    mpl.cm.cool
]
perco_idx = [127,200]

''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize

def save_anno_fig( anno ):
    wf.save_fig( fig_dir, file_types, dots, output_file_name, anno,
        subfolder_save=subfolder )
    
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
# should use polyval()
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
# phi_gb = 0.5801 * na_ratio_3 - 0.5273
phi_gb = np.polyval( P_phi, na_3_gb )
# 100% pr3+ : 0.6652, -0.622
# phi_gb = 0.6652 * na_ratio_3 - 0.622

# predicting phis (Sp. Chg. Pots.) for misor angs in experiment
# fit phi vs angle
P_phi_gb_exp = np.polyfit( mack_ang, phi_gb, 3 )

# apply fit to experimentally measured angles to get experimental phis
phi_gb_exp = np.polyval( P_phi_gb_exp, ema )

# polynomial function of log10( sig_gb/sig_gr ) vs. na
log10_sig_gb_gr = np.polyval( P_cond, na_3_gb )

# evaluate Ea at each [solute]_gb
ea_gb = np.polyval( P_ea, na_3_gb )


# GENERATE FIGURES #####
mpl_customizations()
pl.close( 'all' )

# length fraction vs. space charge potential ##
fidx = 0
pl.figure( figsize=fig_size ) # ( w, h ) inches

# pl.plot( phi_gb, mack, ls='-', c=wf.colors('dark_grey') )
pl.plot( phi_gb, mack, ls='-', c='maroon' )
ax = pl.gca()
ax.set_xlabel( labs[fidx][0][0], labelpad=0.5 )
ax.set_ylabel( labs[fidx][0][1], labelpad=0.5 )
ax.set_xlim( x_lims[fidx] )
ax.set_ylim( y_lims[fidx] )
ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( .4 ) )
ax.minorticks_on()
pl.tight_layout()

# inset axes
ax = pl.axes([ .35, .55, .3, .3 ]) # [ L, B, W, H ] relative to figure
t = phi_gb_exp
s = [ 7**2 for n in range( len( t ) ) ] # [2]
pl.scatter( ema, t, s=s, c=phi_gb_exp, cmap=cmaps[fidx] )
# pl.colorbar()
ax.set_xlabel( labs[fidx][1][0], labelpad=0.5 )
ax.set_ylabel( labs[fidx][1][1], labelpad=0.5 )
ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( 20 ) )
ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( .4 ) )
# ax.set_xlim( x_lims[1] )
ax.set_ylim( y_lims[1] )
ax.minorticks_on()
pl.tight_layout() # can run once to apply to all subplots, i think

anno = name_ext[fidx]
if save:
    save_anno_fig( anno )


# color map for inset in previous figure
fidx += 1
pl.figure( figsize=fig_size ) # ( w, h ) inches
# pl.plot( mack_ang, phi_gb, ls='-' )
t = phi_gb_exp
s = [ 7**2 for n in range( len( t ) ) ] # [2]
pl.scatter( ema, t, s=s, c=phi_gb_exp, cmap=cmaps[fidx] )
pl.colorbar()     

ax = pl.gca()
ax.set_xlabel( labs[fidx][0], labelpad=0.5 )
ax.set_ylabel( labs[fidx][1], labelpad=0.5 )  
pl.tight_layout() # can run once to apply to all subplots, i think

anno = name_ext[fidx]
if save:
    save_anno_fig( anno )


# length fraction vs. na_3_gb ##
fidx += 1
pl.figure( figsize=(3.5,3) ) # ( w, h ) inches

# pl.plot( log10_sig_gb_gr, mack, ls='-', c='maroon' )
t = na_3_gb * 100
s = [ 7**1.5 for n in range( len( t ) ) ] # [2]
pl.scatter( t, mack, s=s, c=t, cmap=cmaps[fidx], edgecolors='none' )
pl.colorbar()

ax = pl.gca()
ax.set_xlabel( labs[fidx][0], labelpad=0.5 )
ax.set_ylabel( labs[fidx][1], labelpad=0.5 )
# ax.set_xlim( x_lims[0] )
ax.set_ylim( y_lims[0] )
ax.minorticks_on()
pl.tight_layout()

anno = name_ext[fidx]
if save:
    save_anno_fig( anno )


# 4. length fraction vs. ea_gb ##
fidx += 1
pl.figure( figsize=(3.5,3) ) # ( w, h ) inches

# pl.plot( log10_sig_gb_gr, mack, ls='-', c='maroon' )
t = ea_gb
s = [ 7**1.5 for n in range( len( t ) ) ] # [2]
pl.scatter( t, mack, s=s, c=t, cmap=cmaps[fidx], edgecolors='none' )
pl.colorbar()

ax = pl.gca()
ax.set_xlabel( labs[fidx][0], labelpad=0.5 )
ax.set_ylabel( labs[fidx][1], labelpad=0.5 )
# ax.set_xlim( x_lims[0] )
ax.set_ylim( y_lims[0] )
ax.minorticks_on()
pl.tight_layout()

# inset axes
ax = pl.axes([ .44, .57, .3, .3 ]) # [ L, B, W, H ] relative to figure
# t = phi_gb_exp
# s = [ 7**2 for n in range( len( t ) ) ] # [2]
pl.scatter( t, mack, s=s, c=t, cmap=cmaps[fidx], edgecolors='none' )
pl.plot( t[ perco_idx[0]:perco_idx[1] ], mack[ perco_idx[0]:perco_idx[1] ], 'o',
    c='w', markersize=1.5 )
print( np.sum( mack[ perco_idx[0]:perco_idx[1] ] ) / np.sum( mack ) )
# pl.colorbar()
ax.set_xlabel( labs[fidx][0], labelpad=0.5 )
ax.set_ylabel( labs[fidx][1], labelpad=0.5 )
ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( .1 ) )
ax.set_xlim( lims[fidx][1][0] )
ax.set_ylim( lims[fidx][1][1] )
ax.minorticks_on()
pl.tight_layout() # can run once to apply to all subplots, i think

anno = name_ext[fidx]
if save:
    save_anno_fig( anno )


# 5. length fraction vs. sig_gb/sig_gr ##
fidx += 1
pl.figure( figsize=(3.5,3) ) # ( w, h ) inches

# pl.plot( log10_sig_gb_gr, mack, ls='-', c='maroon' )
t = log10_sig_gb_gr
s = [ 7**1.5 for n in range( len( t ) ) ] # [2]
pl.scatter( t, mack, s=s, c=t, cmap=cmaps[fidx], edgecolors='none' )
pl.colorbar()

ax = pl.gca()
ax.set_xlabel( labs[fidx][0], labelpad=0.5 )
ax.set_ylabel( labs[fidx][1], labelpad=0.5 )
# ax.set_xlim( x_lims[0] )
ax.set_ylim( y_lims[0] )
ax.minorticks_on()
pl.tight_layout()

# inset axes
ax = pl.axes([ .34, .57, .3, .3 ]) # [ L, B, W, H ] relative to figure
# t = phi_gb_exp
# s = [ 7**2 for n in range( len( t ) ) ] # [2]
pl.scatter( t, mack, s=s, c=t, cmap=cmaps[fidx], edgecolors='none' )
pl.plot( t[ perco_idx[0]:perco_idx[1] ], mack[ perco_idx[0]:perco_idx[1] ], 'o',
    c='w', markersize=1.5 )
# pl.colorbar()
ax.set_xlabel( labs[fidx][0], labelpad=0.5 )
ax.set_ylabel( labs[fidx][1], labelpad=0.5 )
ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( 1 ) )
ax.set_xlim( lims[fidx][1][0] )
ax.set_ylim( lims[fidx][1][1] )
ax.minorticks_on()
pl.tight_layout() # can run once to apply to all subplots, i think
            
anno = name_ext[fidx]
if save:
    save_anno_fig( anno )

'''
REFS
[1] http://stackoverflow.com/questions/17682216/scatter-plot-and-color-mapping-
    in-python
[2] http://stackoverflow.com/questions/14827650/pyplot-scatter-plot-marker-size
'''