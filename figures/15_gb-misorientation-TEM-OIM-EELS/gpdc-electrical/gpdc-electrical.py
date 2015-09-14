''' ########################### OVERVIEW ########################### '''
'''
Created 2015-09-07 by Will Bowman. This creates a figure with complex impedance
spectra from GPDC, and GB conductivity for GPDC and GDC
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
# this is the name of the figure working directory. the output figure will be
# saved here with a file name containing the directory name
fig_dir = 'gpdc-electrical'
# this is the full path to figure directory (for reading data and writing files)
figs_dir = 'C:/Users/willb/Dropbox/WillB/Crozier_Lab/Writing/2015_gb misorientation OIM EELS/figures/' + fig_dir + '/'

# sp0: GPDC Nyquist
d_0 = figs_dir + 'GPDC_200C_fitted_140305.txt'
d_0_skiprows = 1

# sp1: GPDC and GDC boundary conductivity
d_1 = figs_dir + 'Gpdc_CalculatedConductivityErr.txt'
d_1_skiprows = 1
d_2 = figs_dir + 'Gdc2b_CalculatedConductivityErr.txt'
d_2_skiprows = 1

# font size, resolution (DPI), file type, fig_size
# create a figure of size ( width", height" )
# font_size, dots, file_type, fig_size = 10, [ 300, 1200 ], 'png', ( 3.33, 4 )
font_size, dots, file_type, fig_size = 10, [ 300, 1200 ], 'png', ( 3.33, 4 )
# sub_plots = ( 2, 1, 1 ) # suplot 0 ( sub_y, sub_x, sub_i )

# subplot 0 (sp0): length fraction v misorientation angle
sp0_ax_labs = [ 'Z$_{Real}$ ($\Omega$)', 'Z$_{Imag.}$ ($\Omega$)' ]
sp0_entries = ( 'Data', 'Fit' ) # legend entries
sp0_c = [ 'maroon', 'grey' ] # line colors
sp0_m, sp0_m_width = [ 'o', None ], 1 # markers
sp0_ls = [ '', '-' ] # line styles (use '' instead of None)
sp0_lims = [ [ 0, 2.5e5 ], [ 0, 1.5e5 ] ] # x, y axis limits
sp0_maj_loc = [ 0.5e5, 0.5e5 ] # [x,y] major tick locators
sp0_leg_loc = 'upper right'

# subplot1 (sp1): length fraction v concentration
sp1_ax_labs = [ r'10$^3 T^{-1} (K^{-1})$', r'$\sigma_{G.B.}$ (S $cm^{-1})$' ]
sp1_entries = ( '(Pr,Gd)-CeO$_2$', 'Gd-CeO$_2$' )
sp1_c = [ 'maroon', 'grey' ] # line colors
sp1_m, sp1_m_width = [ '^', 'o' ], 1 # markers
sp1_ls = [ '', '' ] # line styles (use '' instead of None)
sp1_lims = [ [ 1.5, 3.0 ], [ 1e-12, 1e-7 ] ] # axis limits
sp1_maj_loc = [ 0.5, 1e-2 ] # [x,y] major tick locators
sp1_leg_loc = 'upper right'


''' ########################### FUNCTIONS ########################### '''

def mpl_customizations():
    wf.wills_mpl( font_size ) # pass the figure's fontsize
    # wf.slide_art_styles()
    # mpl.rc( 'font', family='serif', serif='Times New Roman', weight='normal' )
    mpl.rc( 'font', family='sans-serif', serif='Helvetica', weight='normal' )
    mpl.rc( 'lines', ls='', mew=0.01, markersize=4 )
    mpl.rc( 'legend', numpoints=1, handletextpad=0.5, borderpad=0.5 )

def sp0_style( ax ):
    wf.ax_limits( sp0_lims )
    pl.minorticks_on()
    wf.ax_labels( sp0_ax_labs )
    wf.major_ticks( ax, sp0_maj_loc, scientific=True )
    pl.legend( sp0_entries, loc=sp0_leg_loc ) # locate legend x,y from bottom left
    # ax.yaxis.set_ticklabels([]) # y tick labels off
    # ax.set_yticks([]) # no ticks

def sp1_style( ax ):
    wf.ax_limits( sp1_lims )
    pl.minorticks_on()
    wf.ax_labels( sp1_ax_labs )
    ax.set_yscale( 'log' )
    # wf.major_ticks( ax, sp1_maj_loc )
    pl.legend( sp1_entries, loc=sp1_leg_loc ) # locate legend x,y from bottom left
    # ax.yaxis.set_ticklabels([]) # y tick labels off
    # ax.set_yticks([])


''' ########################### MAIN SCRIPT ########################### '''

# read data, skip header rows
sp0_x0, sp0_y0, sp0_x1, sp0_y1 = np.loadtxt( d_0, skiprows=d_0_skiprows ).T
a, sp1_x0, sp1_y0, sp1_y1, sp1_y2, sp1_y3 = np.loadtxt( d_1, skiprows=d_1_skiprows ).T
b, sp1_x1, sp1_y4, sp1_y5, sp1_y6, sp1_y7 = np.loadtxt( d_2, skiprows=d_2_skiprows ).T

pl.close( 'all' ) # close all open figures
pl.figure( figsize = fig_size ) # create a figure of size ( width", height" )
ax = pl.gca() # store current axis

mpl_customizations() # apply customizations to matplotlib

pl.subplot( 2, 1, 1 ) # suplot 0 ( sub_y, sub_x, sub_i )
ax0 = pl.gca()
pl.plot( sp0_x0, sp0_y0, c=sp0_c[0], marker=sp0_m[0], ls=sp0_ls[0] )
pl.plot( sp0_x1, sp0_y1, c=sp0_c[1], marker=sp0_m[1], ls=sp0_ls[1] )
sp0_style( ax0 )

pl.subplot( 2, 1, 2 ) # suplot 1 ( sub_y, sub_x, sub_i )
ax1 = pl.gca()
pl.errorbar( sp1_x0, sp1_y2, sp1_y3, c=sp1_c[0], marker=sp1_m[0], ls=sp1_ls[0] )
pl.errorbar( sp1_x1, sp1_y6, sp1_y7, c=sp1_c[1], marker=sp1_m[1], ls=sp1_ls[1] )
sp1_style( ax1 )

# applies to all subplots, h_pad defined vertical spacing
pl.tight_layout( pad=0.3, h_pad=0.6 )

# output file info
output_dir = figs_dir
output_file = fig_dir

for dot in dots:
    output_name = wf.save_name( figs_dir, output_file, dot, file_type )
    pl.savefig( output_name, format = file_type, dpi = dot, transparent = True )

''' ########################### REFERENCES ########################### '''