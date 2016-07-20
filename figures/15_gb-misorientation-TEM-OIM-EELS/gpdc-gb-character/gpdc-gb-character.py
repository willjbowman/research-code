''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-09-03 by Will Bowman. This creates a figure with GPDC boundary 
 composition and character data 
'''

''' ########################### IMPORT MODULES ########################### '''
import add_modules_to_syspath # put ~/wills_modules in pyzo path variable
import numpy as np
import pylab as pl
import matplotlib as mpl
import wills_functions as wf
import csv, imp, os
import math as math

##


''' ########################### USER-DEFINED ########################### '''
# path to data file (make gui to pick files?)
fig_dir = 'C:/Users/Besitzer/Dropbox/WillB/Crozier_Lab/Writing/15_WJB_gb misorientation OIM EELS/figures/gpdc-gb-character/'

# misorientation angle distribution (MAD)
d_mad = fig_dir + 'misorientation-distribution/GPDCfib_gbLengthFraction.txt'
d_mad_skiprows = 1
# coincidence site lattice (CSL)
d_csl = fig_dir + 'misorientation-distribution/GPDCfib_cslLengthFraction.txt'
d_csl_skiprows = 0
# mackenzian distribution
d_mack = fig_dir + 'misorientation-distribution/mackenzie_200_bins-tdl.txt'
d_mack_skiprows = 7

# output file info
output_dir = fig_dir
output_file = 'gpdc-gb-character'

# font size, resolution (DPI), file type
fsize, dots, file_type = 10, [ 300, 1200 ], 'png'

# subplot 0 (sp0): length fraction v misorientation angle
sp0_ax_labs = [ 'Misorientation angle (Deg.)', 'Length fraction' ]
sp0_entries = ( 'Experiment', 'Mackenzian\n(isotropic)' ) # legend
sp0_c = [ 'maroon', 'grey' ] # line colors
sp0_m, m_width = [ 'o' ], 1 # markers
sp0_lims = [ [ -2, 67 ], [ 0, 0.2 ] ] # x, y axis limits
sp0_maj_loc = [ 15, 0.1 ] # [x,y] major tick locators
sp0_leg_loc = 'upper left'
mack_scalar, mack_shift = 14, -0.004

# subplot1 (sp1): length fraction v concentration
sp1_ax_labs = [ 'Conicidence site lattice (CSL) $\Sigma$', 'Length fraction' ]
sp1_entries = ( 'Pr', 'Gd', 'Ce' )
sp1_c = [ 'maroon' ] # line colors
sp1_lims = [ [ 0, 50 ], [ 0, 0.07 ] ] # axis limits
sp1_maj_loc = [ 5, 0.02 ] # [x,y] major tick locators
sp1_leg_loc = 'best'
bar_shift = -0.4 # can this be a wf.module


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( fsize ) # pass the figure's fontsize
    # wf.nanoletters_mpl()
    mpl.rc( 'font', family='sans-serif', serif='Helvetica', weight='normal' )
    mpl.rc( 'lines', ls='', mew=0.01, markersize=4 )
    mpl.rc( 'legend', numpoints=1, handletextpad=0.5, borderpad=0.5 )

def sp0_style( ax ):
    wf.ax_limits( sp0_lims )
    pl.minorticks_on()
    wf.ax_labels( sp0_ax_labs, 0.5 )
    wf.major_ticks( ax, sp0_maj_loc )
    pl.legend( sp0_entries, loc=sp0_leg_loc ) # locate legend x,y from bottom left
    # ax.yaxis.set_ticklabels([]) # y tick labels off

def sp1_style( ax ):
    wf.ax_limits( sp1_lims )
    pl.minorticks_on()
    wf.ax_labels( sp1_ax_labs, 0.5 )
    wf.major_ticks( ax, sp1_maj_loc )
    # pl.legend( sp1_entries, loc=sp1_leg_loc ) # locate legend x,y from bottom left


''' ########################### MAIN SCRIPT ########################### '''

# read data, skip header rows
mad_ang, mad = np.loadtxt( d_mad, skiprows=d_mad_skiprows ).T

csl_len = np.loadtxt( d_csl, skiprows=d_csl_skiprows ).T
csl_sig = np.linspace( 1, 49, 49 )

mack_ang, mack_cor, mack_rand = np.loadtxt( d_mack, skiprows=d_mack_skiprows ).T
mack = mack_rand * mack_scalar + mack_shift

pl.close( 'all' ) # close all open figures
pl.figure( figsize = ( 3.33, 4 ) ) # create a figure of size ( width", height" )
ax = pl.gca() # store current axis

mpl_customizations() # apply customizations to matplotlib

pl.subplot( 2, 1, 1 ) # suplot 0 ( sub_y, sub_x, sub_i )
ax0 = pl.gca()
pl.plot( mad_ang, mad, c=sp0_c[0], marker=sp0_m[0] )
pl.plot( mack_ang, mack, c=sp0_c[1], ls='-' )
sp0_style( ax0 )

pl.subplot( 2, 1, 2 ) # suplot 1 ( sub_y, sub_x, sub_i )
ax1 = pl.gca()
pl.bar( csl_sig + bar_shift, csl_len, color=sp1_c[0], alpha=0.5 )
sp1_style( ax1 )

# applies to all subplots, h_pad defined vertical spacing
pl.tight_layout( pad=0.3, h_pad=0.6 )

# for dot in dots:
#     output_name = wf.save_name( fig_dir, output_file, dot, file_type )
#     pl.savefig( output_name, format = file_type, dpi = dot, transparent = True )
    
''' ########################### REFERENCES ########################### '''