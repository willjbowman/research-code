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

##


''' ########################### USER-DEFINED ########################### '''
# path to data file (make gui to pick files?)
data_dir = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_gb misorientation OIM EELS/figures/gpdc-gb-concentration/'

# concentration data; 
d_conc_ang = data_dir + 'gpdc-gb-conc-v-angle_150828.txt'
d_length_conc = data_dir + 'gpdc-gb-length-v-conc_150903.txt'

# output file info
output_dir = data_dir
output_file = 'gpdc-gb-concentration'

# font size, resolution (DPI), file type
fsize, dots, file_type = 10, [300,1200], 'png'

# subplot 0 (sp0): concentration v angle plot
sp0_x_lab, sp0_y_lab = 'Misorientation angle (Deg.)', 'Concentration (Mole frac.)'
sp0_entries = ( 'CeGr.', 'CeG.B.', 'GdGr.', 'GdG.B.', 'PrGr.', 'PrG.B.' ) # legend
sp0_c = [ 'maroon', wf.hex_gold(), 'black' ] # line colors
sp0_m = [ 'o', 'D', 's' ] # markers
sp0_x, sp0_y = [ 15, 65 ], [ 0, 1 ] # axis limits
sp0_maj_loc = [ 10, None ] # [x,y] major tick locators

# subplot1 (sp1): length fraction v concentration
sp1_x_lab, sp1_y_lab = 'Concentration (Mole fract.)', 'Length frac.'
sp1_entries = ( 'Pr', 'Gd', 'Ce' )
sp1_c = [ 'black', wf.hex_gold(), 'maroon' ] # line colors
sp1_x, sp1_y = [ 15, 65 ], [ 0, 1 ] # axis limits
# sp1_maj_loc = [ 10, None ] # [x,y] major tick locators
# x_tick_labs = [ None, -4 , -2, 0, 2, 4 ] # tick labels
conc_y = [ 0, 1 ]


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl()
    # wf.nanoletters_mpl()
    mpl.rc( 'font', family='sans-serif', serif='Helvetica', weight='normal',size=fsize )
    mpl.rc( 'lines', linewidth=1.0, mew=0.01, markersize=3 )
    mpl.rc( 'legend', borderpad = 0.1, labelspacing = 0.1 )

def sp0_style( ax ):
    # pl.xlim( eels_x )
    # pl.ylim( eels_y )
    # pl.minorticks_on()
    # ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( eels_x_maj_loc ) )
    # ax.yaxis.set_ticklabels([]) # y tick labels off

def sp1_style( ax ):
    # pl.ylim( conc_y )
    # pl.minorticks_on()
    # ax.xaxis.set_major_locator( mpl.ticker.MultipleLocator( conc_x_maj_loc ) )
    # ax.yaxis.set_major_locator( mpl.ticker.MultipleLocator( conc_y_maj_loc ) )
    # ax.xaxis.set_ticklabels( x_tick_labs ) # x tick labels


''' ########################### MAIN SCRIPT ########################### '''
# read data, skip header rows
angle, ce_gr, ce_gb, ce_av, pr_gr, pr_gb, _pr_av, gd_gr, gd_gb, gd_av = np.loadtxt( d_conc_ang, skiprows = 1 ).T
conc_bin, pr_len, gd_len, ce_len = np.loadtxt( d_length_conc, skiprows = 1 ).T

pl.close( 'all' ) # close all open figures
pl.figure( figsize = ( 3.33, 6.66 ) ) # create a figure of size ( width", height" )
ax = pl.gca() # store current axis

wf.mpl_customizations() # apply customizations to matplotlib
# wf.slide_art_styles() # figure styling

pl.subplot( 2, 1, 1 ) # ( sub_y, sub_x, sub_i )
ax1 = pl.gca()
pl.plot( d_ev, stack( d_off, d_on ), c=c_eels )
pl.plot( d_ev, d_on, c=c_eels, dashes=ls_on )
eels_style( ax1 )
pl.ylabel( eels_y_lab, labelpad=0.5 )
pl.legend( eels_entries, loc='upper center', fontsize=fsize )

pl.subplot( 2, 1, 2 ) # ( sub_y, sub_x, sub_i )
ax2 = pl.gca()
pl.plot( e_ev, stack( e_off, e_on ), c=c_eels )
pl.plot( e_ev, e_on, c=c_eels, dashes=ls_on )
eels_style( ax2 )
pl.xlabel( eels_x_lab, labelpad=0.3 )

# applies to all subplots, h_pad defined vertical spacing
pl.tight_layout( pad=0.3, h_pad=0.6 )

for dot in dots:
    output_name = wf.save_name( data_dir, output_file, dot, file_type )
    pl.savefig( output_name, format = file_type, dpi = dot, transparent = True )
    
''' ########################### REFERENCES ########################### '''