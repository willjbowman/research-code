''' ########################### OVERVIEW ########################### '''
'''
 Created 2015-09-02 by Will Bowman. This creates a figure with eels data and 
 composition profiles 
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
data_dir = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_gb misorientation OIM EELS/figures/gpdc-gb-eels/'

# d: 140203 SI-02; e: 140729 SI-11; f: 140203 SI-08
eels_d = data_dir + 'eels-data/140203_3aGPDCfib_EELSSI2_highloss_gbAB.txt'
eels_e = data_dir + 'eels-data/140729_gpdcFIB_EELSSI-12_gb5.txt'
eels_f = data_dir + 'eels-data/140203_3aGPDCfib_EELSSI8_highloss_gbAE.txt'

conc_g = data_dir + 'composition-profiles/140203_3aGPDCfib_EELSSI2_highloss_gbAB_1LO.txt'
conc_h = data_dir + 'composition-profiles/140729_gpdcFIB_EELSSI-11_gb5_1FH.txt'
conc_i = data_dir + 'composition-profiles/140203_3aGPDCfib_EELSSI8_highloss_gbAE_1OP.txt'

# output file info
output_dir = data_dir
output_file = 'gpdc-gb-eels_d-i'

dots, file_type = 300, 'png' # output file resolution (DPI), file type

# eels plots
eels_x_lab, eels_y_lab = 'Energy loss (eV)', 'Counts\n(Arb. units)'
eels_entries = ( 'Grain', 'G.B.' )
eels_x, eels_y = [ 860, 1250 ], [ -1e3, None ]
c_eels, ls_on = 'maroon', (4,1)
percent_shift = 200
eels_x_maj_loc = 100

# concentration profiles
conc_x_lab, conc_y_lab = 'Distance (nm)', 'Concentration\n(Mole frac.)'
conc_entries = ( 'Ce', 'Gd', 'Pr' )
g_conc_x, h_conc_x, i_conc_x, ticks_x = [ 5, 15 ], [ 3, 13 ], [ 3, 13 ], 4
conc_x_maj_loc, conc_y_maj_loc = 2, 1
x_tick_labs = [ None, -4 , -2, 0, 2, 4 ]
g_shift_x, h_shift_x, i_shift_x = 0.5, 1, -0.5
conc_y = [ 0, 1 ]
ce_m, gd_m, pr_m = 'o', 'D', 's'
ce_c, gd_c, pr_c = wf.hex_gold(), 'black', 'grey'

''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    mpl.rcParams[ 'font.size' ] = 10
    
def stack( top_curve, bottom_curve ):
    shifted_top = top_curve + np.max( bottom_curve ) - np.min( bottom_curve )
    return shifted_top

def eels_style( ax ):
    pl.xlim( eels_x )
    pl.ylim( eels_y )
    pl.minorticks_on()
    ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( eels_x_maj_loc ) )
    ax.yaxis.set_ticklabels([]) # y tick labels off

def conc_style( ax ):
    pl.ylim( conc_y )
    pl.minorticks_on()
    ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( conc_x_maj_loc ) )
    ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( conc_y_maj_loc ) )
    ax.xaxis.set_ticklabels( x_tick_labs ) # x tick labels
    
''' ########################### MAIN SCRIPT ########################### '''
# read data, skip header rows
d_ev, d_off, d_on = np.loadtxt( eels_d, skiprows = 2 ).T # REFACTOR THIS
e_ev, e_off, e_on = np.loadtxt( eels_e, skiprows = 2 ).T
f_ev, f_off, f_on = np.loadtxt( eels_f, skiprows = 2 ).T

g_nm, g_pr, g_gd, g_ce = np.loadtxt( conc_g, skiprows = 2 ).T
h_nm, h_pr, h_gd, h_ce = np.loadtxt( conc_h, skiprows = 2 ).T
i_nm, i_pr, i_gd, i_ce = np.loadtxt( conc_i, skiprows = 2 ).T

pl.close( 'all' ) # close all open figures
pl.figure( figsize = ( 7, 2.8 ) ) # create a figure of size ( width", height" )
ax = pl.gca() # store current axis

wf.mpl_customizations() # apply customizations to matplotlib
mpl.rc( 'font', family='sans-serif', serif='Helvetica', weight='normal',size=10 )
mpl.rc( 'lines', linewidth=1.0, mew=0.01, markersize=3 )
mpl.rc( 'legend', borderpad = 0.1, labelspacing = 0.1 )
# wf.slide_art_styles() # figure styling
fontsize = mpl.rcParams[ 'font.size' ]

pl.subplot( 2, 3, 1 ) # ( sub_y, sub_x, sub_i )
ax1 = pl.gca()
pl.plot( d_ev, stack( d_off, d_on ), c=c_eels )
pl.plot( d_ev, d_on, c=c_eels, dashes=ls_on )
eels_style( ax1 )
pl.ylabel( eels_y_lab, labelpad=0.5 )
pl.legend( eels_entries, loc='upper center', fontsize=fontsize )

pl.subplot( 2, 3, 2 ) # ( sub_y, sub_x, sub_i )
ax2 = pl.gca()
pl.plot( e_ev, stack( e_off, e_on ), c=c_eels )
pl.plot( e_ev, e_on, c=c_eels, dashes=ls_on )
eels_style( ax2 )
pl.xlabel( eels_x_lab, labelpad=0.3 )

pl.subplot( 2, 3, 3 ) # ( sub_y, sub_x, sub_i )
ax3 = pl.gca()
pl.plot( f_ev, stack( f_off, f_on ), c=c_eels )
pl.plot( f_ev, f_on, c=c_eels, dashes=ls_on )
eels_style( ax3 )


pl.subplot( 2, 3, 4 ) # ( sub_y, sub_x, sub_i )
ax4 = pl.gca()
pl.plot( g_nm+g_shift_x, g_ce, marker=ce_m, c=ce_c )
pl.plot( g_nm+g_shift_x, g_gd, marker=gd_m, c=gd_c )
pl.plot( g_nm+g_shift_x, g_pr, marker=pr_m, c=pr_c )
pl.xlim( g_conc_x )
conc_style( ax4 )
pl.ylabel( conc_y_lab, labelpad=0.5 )
pl.legend( conc_entries, loc='center left', fontsize=fontsize, numpoints = 3 )


pl.subplot( 2, 3, 5 ) # ( sub_y, sub_x, sub_i )
ax5 = pl.gca()
pl.plot( h_nm+h_shift_x, h_ce, marker=ce_m, c=ce_c )
pl.plot( h_nm+h_shift_x, h_gd, marker=gd_m, c=gd_c )
pl.plot( h_nm+h_shift_x, h_pr, marker=pr_m, c=pr_c )
pl.xlim( h_conc_x )
conc_style( ax5 )
ax5.yaxis.set_ticklabels([]) # y tick labels off
pl.xlabel( conc_x_lab, labelpad=0.3 )


pl.subplot( 2, 3, 6 ) # ( sub_y, sub_x, sub_i )
ax6 = pl.gca()
pl.plot( i_nm+i_shift_x, i_ce, marker=ce_m, c=ce_c )
pl.plot( i_nm+i_shift_x, i_gd, marker=gd_m, c=gd_c )
pl.plot( i_nm+i_shift_x, i_pr, marker=pr_m, c=pr_c )
pl.xlim( i_conc_x )
ax6.yaxis.set_ticklabels([]) # y tick labels off
conc_style( ax6 )

# applies to all subplots, h_pad defined vertical spacing
pl.tight_layout( pad=0.3, h_pad=0.6 )

output_name = wf.save_name( data_dir, output_file, dots, file_type )
pl.savefig( output_name, format = file_type, dpi = dots, transparent = True )
    
''' ########################### REFERENCES ########################### '''